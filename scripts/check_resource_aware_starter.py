from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "starter-kits" / "resource-aware-github"
POLICY = KIT / ".agentic" / "repo-policy.json"
BUNDLED_SCHEMA = KIT / "schemas" / "resource-aware-repo-policy-v1.schema.json"
CANONICAL_SCHEMA = ROOT / "schemas" / "resource-aware-repo-policy-v1.schema.json"
WORKFLOW = KIT / ".github" / "workflows" / "resource-aware-gate.yml"
README = KIT / "README.md"
AGENTS = KIT / "AGENTS.md"
CANARY = KIT / "docs" / "CANARY_PROTOCOL.md"

EXPECTED_FILES = (
    POLICY,
    BUNDLED_SCHEMA,
    CANONICAL_SCHEMA,
    WORKFLOW,
    README,
    AGENTS,
    CANARY,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    for path in EXPECTED_FILES:
        if not path.is_file():
            errors.append(f"missing required starter artifact: {path.relative_to(ROOT)}")

    if errors:
        print("Resource-aware starter self-test failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    try:
        policy = load_json(POLICY)
        bundled_schema = load_json(BUNDLED_SCHEMA)
        canonical_schema = load_json(CANONICAL_SCHEMA)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"Resource-aware starter self-test failed: invalid JSON: {error}")
        return 1

    schema_ref = policy.get("$schema")
    if schema_ref != "../schemas/resource-aware-repo-policy-v1.schema.json":
        errors.append("policy $schema must point to the bundled portable schema")
    else:
        resolved_schema = (POLICY.parent / schema_ref).resolve()
        if resolved_schema != BUNDLED_SCHEMA.resolve():
            errors.append("policy $schema does not resolve to the bundled schema")

    if bundled_schema != canonical_schema:
        errors.append("bundled and canonical policy schemas differ")

    expected_policy_values = {
        ("version",): 1,
        ("work_in_progress", "active_targets"): 1,
        ("work_in_progress", "active_implementation_pull_requests"): 1,
        ("work_in_progress", "parallel_writers_per_branch"): 1,
        ("connector", "lane_first"): True,
        ("connector", "serial_calls"): True,
        ("connector", "max_mutations_per_authorized_cycle"): 1,
        ("connector", "readback_required"): True,
        ("connector", "fetch_successful_logs"): False,
        ("actions", "event_first"): True,
        ("actions", "required_workflows_must_report"): True,
        ("actions", "conditional_expensive_steps"): True,
        ("evidence", "exact_head_required"): True,
        ("evidence", "old_head_may_authorize"): False,
        ("evidence", "technical_green_is_semantic_approval"): False,
        ("merge", "draft_direct_merge_allowed"): False,
        ("merge", "expected_head_required"): True,
        ("merge", "workflow_may_merge"): False,
        ("safety", "privileged_jobs_execute_pull_request_code"): False,
        ("safety", "cross_repository_credentials"): False,
        ("safety", "no_op_commits_for_retries"): False,
    }

    for key_path, expected in expected_policy_values.items():
        current: object = policy
        for key in key_path:
            if not isinstance(current, dict) or key not in current:
                current = None
                break
            current = current[key]
        if current != expected:
            errors.append(f"policy {'.'.join(key_path)} must be {expected!r}")

    stop_statuses = set(policy.get("connector", {}).get("stop_on_http_status", []))
    if not {403, 429}.issubset(stop_statuses):
        errors.append("policy connector.stop_on_http_status must include 403 and 429")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    required_workflow_fragments = (
        "pull_request:",
        "merge_group:",
        "workflow_dispatch:",
        "permissions: {}",
        "contents: read",
        "POLICY_REF: ${{ github.sha }}",
        "EVIDENCE_HEAD: ${{ github.event.pull_request.head.sha || github.sha }}",
        "cancel-in-progress: true",
    )
    for fragment in required_workflow_fragments:
        if fragment not in workflow:
            errors.append(f"workflow missing required fragment: {fragment}")

    forbidden_workflow_fragments = (
        "pull_request_target:",
        "issues: write",
        "pull-requests: write",
        "contents: write",
        "actions: write",
        "merge_pull_request",
    )
    for fragment in forbidden_workflow_fragments:
        if fragment in workflow:
            errors.append(f"workflow contains forbidden fragment: {fragment}")

    readme = README.read_text(encoding="utf-8")
    for path in (
        ".agentic/repo-policy.json",
        ".github/workflows/resource-aware-gate.yml",
        "schemas/resource-aware-repo-policy-v1.schema.json",
        "AGENTS.md",
        "docs/CANARY_PROTOCOL.md",
    ):
        if path not in readme:
            errors.append(f"starter README does not list copied artifact: {path}")

    if errors:
        print("Resource-aware starter self-test failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Resource-aware starter self-test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
