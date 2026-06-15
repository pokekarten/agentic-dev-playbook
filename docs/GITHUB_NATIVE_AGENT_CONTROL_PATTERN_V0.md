# GitHub-native Agent Control Pattern v0

Status: public-safe pattern  
Date: 2026-06-15  
Scope: generic agent-control method; no private project truth

## Purpose

Describe a public-safe pattern for using GitHub as a lightweight control surface for AI-assisted work without requiring private project state, secrets, or automatic write actions.

This pattern is intentionally generic. It does not reference private repositories, private PRs, private issue numbers, product data, branch names, or active project truth.

## Core idea

GitHub can support an auditable agent-control loop:

```text
source evidence -> lease -> agent action -> candidate envelope -> deterministic hash -> validator -> accept/reject/repair
```

The goal is not to create a cryptocurrency or a decentralized blockchain. The goal is to make agent work more reviewable, safer, and less noisy.

## Roles

| Role | Meaning |
|---|---|
| Control repo | Stores public-safe protocol docs and validation examples. |
| Project repo | Stores real project work and project-local truth. |
| Agent slot | A scheduled or manually invoked worker that reads sources and proposes a result. |
| Candidate envelope | A compact JSON object describing the proposed result. |
| Validator | Read-only check that validates shape, scores, and hash recomputation. |
| Sequencer | Human or trusted process that accepts/rejects candidates. |

## Public/private split

Public repositories may contain:

```text
- protocol docs,
- toy examples,
- reusable validators,
- workflow templates,
- public-safe rubrics.
```

Private repositories should contain:

```text
- private project details,
- active PR/issue/CI state,
- private ledger state,
- business-sensitive context,
- raw or detailed operational history.
```

## Minimal candidate envelope

```json
{
  "candidate_version": "candidate-envelope-v0",
  "lane": "demo",
  "slot": "slot00",
  "start_prev_block_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "payload": {
    "block_version": "gh-chain-v0",
    "created_utc": "2026-06-15T00:00:00Z",
    "lane": "demo",
    "payload_ref": "example/repo#1",
    "payload_type": "task_selection",
    "statement": "Selected the next safe validation task."
  },
  "evidence_refs": ["example/repo#1"],
  "terminal_result": "NEXT_UNBLOCKED_TASK_SELECTED",
  "progress_score": 1,
  "evidence_score": 2,
  "risk_score": 1,
  "candidate_hash": "8f589f32d087aede4101cc1a4d41cb7d4c65eaa01742eaf59c34fa225caec704"
}
```

## Hashing rule

Use deterministic canonical JSON before hashing.

The reference Python implementation uses:

```python
json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

This is deterministic for the reference validator. Treat it as a simple v0 rule, not a full cross-language canonicalization standard.

## Evidence rule

A hash is not enough.

```text
hash = integrity of input
evidence = reason to trust the input
```

A candidate should be rejected if it contains only a hash and no reconstructable payload.

## Non-parallel CI rule

Workflows should not become an uncontrolled parallel agent system.

For the public-safe prototype:

```text
- use workflow_dispatch only,
- use permissions: contents: read,
- set a global concurrency group,
- cancel-in-progress: false,
- never write commits/issues/comments/approvals,
- validate toy fixtures only.
```

## Example workflow

See:

```text
.github/workflows/public-agent-control-validation.yml
```

The workflow is manual-only and validates public-safe demo fixtures.

## When to use this pattern

Use it when:

```text
- agent work needs reviewability,
- multiple workers can collide,
- outputs should be scored or rejected,
- public-safe examples help others copy the method.
```

Do not use it when:

```text
- the workflow needs secrets,
- private project truth would be exposed,
- automatic writes are required,
- validation failures would block unrelated product work,
- a simpler checklist would be enough.
```

## Maturity model

```text
A0 manual: humans decide everything.
A1 observable: agents report results.
A2 candidate: agents produce reconstructable candidates or no-block diagnoses.
A3 sequenced: a trusted sequencer accepts/rejects candidates.
A4 adaptive: leases and follow-ups are coordinated safely.
```

Public examples should stay around A2/A3. More autonomy belongs in private, source-backed project control until proven safe.
