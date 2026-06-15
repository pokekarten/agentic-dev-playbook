#!/usr/bin/env python3
"""Generate public-safe demo candidate-envelope fixtures.

The fixtures are intentionally generic and contain no private project truth.
They are generated during the manual workflow run so the repository does not
need to store hash-bearing test data that can drift from the reference code.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def write(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    out = Path("validation-output/generated-fixtures")
    zero = "0" * 64

    valid = {
        "candidate_version": "candidate-envelope-v0",
        "lane": "demo",
        "slot": "slot00",
        "start_prev_block_hash": zero,
        "payload": {
            "block_version": "gh-chain-v0",
            "created_utc": "2026-06-15T00:00:00Z",
            "lane": "demo",
            "payload_ref": "example/repo#1",
            "payload_type": "task_selection",
            "statement": "Selected the next safe validation task.",
        },
        "evidence_refs": ["example/repo#1"],
        "terminal_result": "NEXT_UNBLOCKED_TASK_SELECTED",
        "progress_score": 1,
        "evidence_score": 2,
        "risk_score": 1,
    }
    valid["candidate_hash"] = sha256_json(valid)

    no_block = {
        "candidate_payload": "none",
        "candidate_hash": "none",
        "no_block_reason": "No useful public-safe candidate exists for this demo run.",
        "mainpool_next": "Keep workflow manual and read-only until a stronger example is needed.",
    }

    hash_only = {
        "candidate_hash": valid["candidate_hash"],
    }

    bad_hash = dict(valid)
    bad_hash["candidate_hash"] = zero

    write(out / "valid.json", valid)
    write(out / "no_block.json", no_block)
    write(out / "reject_hash_only.json", hash_only)
    write(out / "reject_bad_hash.json", bad_hash)

    print(f"Generated demo fixtures under {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
