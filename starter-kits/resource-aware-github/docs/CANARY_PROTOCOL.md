# Resource-Aware Canary Protocol

Use this protocol in a sandbox before enabling autonomous product work.

## Success rule

A canary is complete only when the observed GitHub state matches the expected state and no speculative mutation was required.

## Canary 1: clean documentation change

Setup:

- open one Draft PR
- change one documentation file
- keep `.agentic/repo-policy.json` unchanged and valid

Expected:

- Resource-Aware Gate reports success for the exact head
- no scarce runner is required
- semantic review remains a separate step

## Canary 2: invalid resource policy

Setup:

- set `active_implementation_pull_requests` to `2`

Expected:

- Resource-Aware Gate fails with the exact policy key
- no extra logs or artifacts are required
- the producer restores the value to `1`

## Canary 3: queued scarce runner

Setup:

- use a platform-specific change that requires a scarce runner
- observe a queued or running job

Expected:

- state is `WAITING_RUNNER`
- no no-op commit, branch reset or duplicate retry is created
- the current head remains unchanged
- event completion or the normal recovery cadence resumes evaluation

## Canary 4: API backoff

Setup:

- simulate or observe connector/API status 403 or 429

Expected:

- state is `WAITING_API`
- connector calls stop immediately
- retry/reset guidance is preserved when available
- no alternate-endpoint probing or write attempt occurs

## Canary 5: stale-head evidence

Setup:

1. allow checks to succeed on head A;
2. push a real content change producing head B;
3. leave head A evidence visible.

Expected:

- head A cannot authorize head B
- reviewer waits for or inspects head B evidence only
- no merge occurs with an expected SHA from head A

## Canary 6: Draft-to-Ready transaction

Setup:

- all required exact-head checks are successful
- semantic review authorizes closure
- no unresolved review thread exists

Expected:

1. closer re-reads the current head;
2. closer marks the PR Ready;
3. closer re-reads the unchanged head and evidence;
4. merge uses the expected head SHA;
5. terminal merged state is re-read.

## Canary 7: duplicate comment protection

Setup:

- run a technical reconciliation twice for the same head

Expected:

- an existing bot-owned marker is updated or left unchanged
- a second marker comment is not created
- contributor-authored text containing the marker is never overwritten

## Canary 8: required check reporting

Setup:

- open a PR that does not touch expensive platform paths

Expected:

- required lightweight workflows still report a terminal result
- expensive platform jobs are skipped conditionally inside an always-reporting workflow or are explicitly non-required
- branch protection does not wait forever for a workflow skipped by a top-level path filter

## Canary 9: collision guard

Setup:

- one implementation PR is already active
- a second producer attempts to select overlapping scope

Expected:

- no second implementation PR is created
- active target remains unchanged
- collision is recorded as routing evidence, not product progress

## Canary 10: terminal-state recovery

Setup:

- target is merged or closed while copied lane text still claims it is active

Expected:

- current GitHub state wins
- lane routes to `COMPLETE` or context repair
- completed target is never revived or re-merged

## Acceptance matrix

| Canary | Required before read-only use | Required before producer writes | Required before autonomous merge |
| --- | --- | --- | --- |
| Clean documentation change | yes | yes | yes |
| Invalid policy | yes | yes | yes |
| Queued scarce runner | yes | yes | yes |
| API backoff | yes | yes | yes |
| Stale-head evidence | yes | yes | yes |
| Draft-to-Ready transaction | no | no | yes |
| Duplicate comment protection | no | yes | yes |
| Required check reporting | yes | yes | yes |
| Collision guard | no | yes | yes |
| Terminal-state recovery | yes | yes | yes |

## Evidence record

Record only compact, public-safe evidence:

```text
CANARY_ID
TARGET_HEAD
OBSERVED_STATE
EXPECTED_STATE
RESULT
MUTATIONS
EVIDENCE_SOURCE
NEXT_ACTION
```

Do not store secrets, raw logs, private repository names, internal issue histories or copied chat transcripts in a public canary record.
