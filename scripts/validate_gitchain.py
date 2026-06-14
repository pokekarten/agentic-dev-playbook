from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

JSON_PATHS = [
    ROOT / "examples" / "gitchain-commitment-v0.json",
    ROOT / "examples" / "gitchain-wallet-v0.json",
    ROOT / "examples" / "gitchain-wallet-balance-v0.json",
    ROOT / "examples" / "gitchain-node-manifest-v0.json",
    ROOT / "examples" / "gitchain-block-producer-v0.json",
    ROOT / "examples" / "gitchain-cycle-block-v0.json",
    ROOT / "examples" / "gitchain-reputation-event-v0.json",
    ROOT / "examples" / "gitchain-task-block-v0.json",
    ROOT / "gitchain" / "node.json",
    ROOT / "gitchain" / "wallet.json",
]

EXPECTED_KINDS = {
    "gitchain-commitment-v0.json": "GITCHAIN_COMMITMENT",
    "gitchain-wallet-v0.json": "GITCHAIN_WALLET",
    "gitchain-wallet-balance-v0.json": "GITCHAIN_WALLET_BALANCE",
    "gitchain-node-manifest-v0.json": "GITCHAIN_NODE",
    "gitchain-block-producer-v0.json": "GITCHAIN_BLOCK_PRODUCER",
    "gitchain-cycle-block-v0.json": "GITCHAIN_CYCLE_BLOCK",
    "gitchain-reputation-event-v0.json": "GITCHAIN_REPUTATION_EVENT",
    "gitchain-task-block-v0.json": "TASK_BLOCK",
    "node.json": "GITCHAIN_NODE",
    "wallet.json": "GITCHAIN_WALLET",
}

HASH_RE = re.compile(r"^sha256:([A-Za-z0-9._:-]+|null)$")

DISALLOWED_MARKERS = {
    "api_key=",
    "apikey=",
    "password=",
    "secret=",
    "token=",
    "private_key=",
    "begin private key",
    "begin rsa private key",
    "begin openssh private key",
}

PRIVATE_SAFETY_KEYS = (
    "contains_private_message",
    "contains_secret",
    "contains_personal_data",
    "contains_private_project_state",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"{rel(path)}: missing")
        return None

    raw = path.read_text(encoding="utf-8")
    lower = raw.lower()
    for marker in sorted(DISALLOWED_MARKERS):
        if marker in lower:
            errors.append(f"{rel(path)}: contains high-signal restricted marker: {marker}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(path)}: invalid JSON: {exc}")
        return None

    if not isinstance(data, dict):
        errors.append(f"{rel(path)}: top-level JSON value must be an object")
        return None

    return data


def require_fields(path: Path, data: dict[str, Any], fields: list[str], errors: list[str]) -> None:
    for field in fields:
        if field not in data:
            errors.append(f"{rel(path)}: missing required field {field!r}")


def require_hash(path: Path, data: dict[str, Any], field: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, str) or not HASH_RE.match(value):
        errors.append(f"{rel(path)}: {field!r} must look like sha256:<value>")


def check_kind(path: Path, data: dict[str, Any], errors: list[str]) -> None:
    expected = EXPECTED_KINDS.get(path.name)
    if expected is None:
        return

    if data.get("kind") != expected:
        errors.append(f"{rel(path)}: kind must be {expected!r}, got {data.get('kind')!r}")

    if data.get("version") != "v0":
        errors.append(f"{rel(path)}: version must be 'v0'")


def check_public_safety(path: Path, data: dict[str, Any], errors: list[str]) -> None:
    public_safety = data.get("public_safety")
    if not isinstance(public_safety, dict):
        return

    for key in PRIVATE_SAFETY_KEYS:
        if key in public_safety and public_safety[key] is not False:
            errors.append(f"{rel(path)}: public_safety.{key} must be false")


def canonical_hash_without_self(data: dict[str, Any]) -> str:
    payload = dict(data)
    payload.pop("block_hash", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def check_live_node(errors: list[str]) -> None:
    node_path = ROOT / "gitchain" / "node.json"
    wallet_path = ROOT / "gitchain" / "wallet.json"

    node = load_json(node_path, errors)
    wallet = load_json(wallet_path, errors)

    if node is None or wallet is None:
        return

    check_kind(node_path, node, errors)
    check_kind(wallet_path, wallet, errors)

    require_fields(
        node_path,
        node,
        ["kind", "version", "node_id", "operator", "wallet_id", "ledger_path", "capabilities", "private_data_policy"],
        errors,
    )
    require_fields(
        wallet_path,
        wallet,
        ["kind", "version", "wallet_id", "owner", "transferable", "monetary_value", "balance_source", "public_safety"],
        errors,
    )

    if node.get("wallet_id") != wallet.get("wallet_id"):
        errors.append("gitchain/node.json and gitchain/wallet.json must use the same wallet_id")

    if wallet.get("transferable") is not False:
        errors.append("gitchain/wallet.json: transferable must be false")

    if wallet.get("monetary_value") is not False:
        errors.append("gitchain/wallet.json: monetary_value must be false")

    private_policy = node.get("private_data_policy", {})
    for key in ("publish_private_messages", "publish_private_salts", "publish_private_project_state"):
        if private_policy.get(key) is not False:
            errors.append(f"gitchain/node.json: private_data_policy.{key} must be false")


def check_cycle_block(path: Path, data: dict[str, Any], errors: list[str]) -> None:
    require_fields(
        path,
        data,
        [
            "kind",
            "version",
            "height",
            "cycle_id",
            "previous_block_hash",
            "commitment_root",
            "policy_hash",
            "schema_version",
            "producer_id",
            "producer_wallet_id",
            "commitments",
            "proof",
            "timestamp",
            "public_safety",
        ],
        errors,
    )

    if data.get("kind") != "GITCHAIN_CYCLE_BLOCK":
        errors.append(f"{rel(path)}: kind must be 'GITCHAIN_CYCLE_BLOCK'")

    if not isinstance(data.get("height"), int) or data["height"] < 0:
        errors.append(f"{rel(path)}: height must be a non-negative integer")

    for field in ("previous_block_hash", "commitment_root", "policy_hash"):
        require_hash(path, data, field, errors)

    if not isinstance(data.get("commitments"), list):
        errors.append(f"{rel(path)}: commitments must be a list")

    proof = data.get("proof")
    if not isinstance(proof, dict):
        errors.append(f"{rel(path)}: proof must be an object")
    else:
        for key in ("public_safety_valid", "schema_valid", "policy_hash_known", "previous_block_hash_linked"):
            if proof.get(key) is not True:
                errors.append(f"{rel(path)}: proof.{key} must be true")

        proof_hash = proof.get("proof_hash")
        if not isinstance(proof_hash, str) or not HASH_RE.match(proof_hash):
            errors.append(f"{rel(path)}: proof.proof_hash must look like sha256:<value>")

    if "block_hash" in data:
        expected = canonical_hash_without_self(data)
        if data["block_hash"] != expected:
            errors.append(f"{rel(path)}: block_hash mismatch; expected {expected}")


def check_all_json_examples(errors: list[str]) -> None:
    for path in JSON_PATHS:
        data = load_json(path, errors)
        if data is None:
            continue
        check_kind(path, data, errors)
        check_public_safety(path, data, errors)

    for block_path in sorted((ROOT / "gitchain" / "blocks").glob("*.json")):
        data = load_json(block_path, errors)
        if data is None:
            continue
        check_public_safety(block_path, data, errors)
        check_cycle_block(block_path, data, errors)


def main() -> int:
    errors: list[str] = []

    check_all_json_examples(errors)
    check_live_node(errors)

    if errors:
        print("GitChain validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GitChain validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
