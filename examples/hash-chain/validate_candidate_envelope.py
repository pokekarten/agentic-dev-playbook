#!/usr/bin/env python3
"""Public-safe candidate-envelope-v0 validator example.

This is a toy/reference validator for public documentation and workflow demos.
It does not call GitHub APIs, read secrets, mutate state, create comments, or
validate private project truth. It only validates local JSON fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

LANES = {"demo"}
CANDIDATE_VERSION = "candidate-envelope-v0"
BLOCK_VERSION = "gh-chain-v0"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_TERMINAL_RESULTS = {
    "MERGED",
    "FILE_CHANGED",
    "ISSUE_UPDATED",
    "PR_OPENED",
    "CLOSED",
    "PATCH_READY",
    "NEXT_UNBLOCKED_TASK_SELECTED",
}
ALLOWED_PAYLOAD_TYPES = {
    "bot_result",
    "gate_result",
    "task_selection",
    "work_result",
    "learning_note",
    "health_note",
    "manual_note",
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\b(api[_-]?key|password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"),
]


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def fail(message: str) -> None:
    raise ValueError(message)


def assert_hex64(value: Any, field: str) -> None:
    if not isinstance(value, str) or not HEX64_RE.fullmatch(value):
        fail(f"{field} must be a 64-character lowercase hex SHA-256 hash")


def assert_score(value: Any, field: str) -> None:
    if not isinstance(value, int) or value < 0 or value > 3:
        fail(f"{field} must be an integer from 0 to 3")


def assert_safe_text(obj: Any) -> None:
    text = canonical(obj)
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            fail(f"potential secret-like value matched safety pattern: {pattern.pattern}")


def validate_payload(payload: Any, lane: str) -> None:
    if not isinstance(payload, dict):
        fail("payload must be an object")
    required = {"block_version", "created_utc", "lane", "payload_ref", "payload_type", "statement"}
    missing = required - set(payload.keys())
    if missing:
        fail(f"payload missing fields: {sorted(missing)}")
    if payload.get("block_version") != BLOCK_VERSION:
        fail(f"payload.block_version must be {BLOCK_VERSION}")
    if payload.get("lane") != lane:
        fail("payload.lane must match candidate lane")
    if payload.get("payload_type") not in ALLOWED_PAYLOAD_TYPES:
        fail(f"invalid payload_type: {payload.get('payload_type')!r}")
    for field in ("created_utc", "payload_ref", "statement"):
        if not isinstance(payload.get(field), str) or not payload.get(field).strip():
            fail(f"payload.{field} must be a non-empty string")
    if len(payload["statement"]) > 500:
        fail("payload.statement must stay compact (<= 500 characters)")


def validate_no_block(obj: dict[str, Any], source: str) -> str:
    if obj.get("candidate_payload") != "none" or obj.get("candidate_hash") != "none":
        fail(f"{source}: no-block object must set candidate_payload and candidate_hash to 'none'")
    if not isinstance(obj.get("no_block_reason"), str) or not obj["no_block_reason"].strip():
        fail(f"{source}: no_block_reason must be a non-empty string")
    if not isinstance(obj.get("mainpool_next"), str) or not obj["mainpool_next"].strip():
        fail(f"{source}: mainpool_next must be a non-empty string")
    assert_safe_text(obj)
    return "NO_BLOCK_OK"


def validate_candidate(obj: dict[str, Any], source: str) -> str:
    if obj.get("candidate_payload") == "none" or obj.get("candidate_hash") == "none":
        return validate_no_block(obj, source)

    required = {
        "candidate_version",
        "lane",
        "slot",
        "start_prev_block_hash",
        "payload",
        "evidence_refs",
        "terminal_result",
        "progress_score",
        "evidence_score",
        "risk_score",
        "candidate_hash",
    }
    missing = required - set(obj.keys())
    if missing:
        fail(f"{source}: candidate missing fields: {sorted(missing)}")

    if obj.get("candidate_version") != CANDIDATE_VERSION:
        fail(f"{source}: candidate_version must be {CANDIDATE_VERSION}")
    lane = obj.get("lane")
    if lane not in LANES:
        fail(f"{source}: invalid lane {lane!r}")
    slot = obj.get("slot")
    if not isinstance(slot, str) or not re.fullmatch(r"slot\d{2}", slot):
        fail(f"{source}: slot must look like slot00")

    assert_hex64(obj.get("start_prev_block_hash"), f"{source}: start_prev_block_hash")
    validate_payload(obj.get("payload"), lane)

    evidence_refs = obj.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs or not all(isinstance(ref, str) and ref.strip() for ref in evidence_refs):
        fail(f"{source}: evidence_refs must be a non-empty list of strings")

    if obj.get("terminal_result") not in ALLOWED_TERMINAL_RESULTS:
        fail(f"{source}: invalid terminal_result {obj.get('terminal_result')!r}")
    for field in ("progress_score", "evidence_score", "risk_score"):
        assert_score(obj.get(field), f"{source}: {field}")

    assert_safe_text(obj)

    claimed_hash = obj.get("candidate_hash")
    assert_hex64(claimed_hash, f"{source}: candidate_hash")
    without_hash = {key: value for key, value in obj.items() if key != "candidate_hash"}
    expected_hash = sha256_json(without_hash)
    if claimed_hash != expected_hash:
        fail(f"{source}: candidate_hash mismatch: expected {expected_hash}, got {claimed_hash}")

    return claimed_hash


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate public-safe candidate-envelope-v0 JSON fixtures.")
    parser.add_argument("paths", nargs="+", help="Candidate JSON files to validate")
    args = parser.parse_args(argv)

    try:
        for path_text in args.paths:
            path = Path(path_text)
            with path.open("r", encoding="utf-8") as handle:
                obj = json.load(handle)
            if not isinstance(obj, dict):
                fail(f"{path}: top-level value must be an object")
            result = validate_candidate(obj, str(path))
            print(f"OK: {path}: {result}")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
