# Resource-Aware GitHub Starter Kit

A copyable baseline for small AI-assisted repositories that need to make progress without treating runner queues, API limits or missing local tools as code defects.

## What this kit provides

- one machine-readable repository policy
- one read-only GitHub Actions gate
- one role contract for AI and connector operators
- one canary protocol for proving the workflow before product work
- one JSON Schema for validating policy files

## Design goals

1. **GitHub is the shared source of truth.** Issues, pull requests, current heads and workflow results override copied status text.
2. **One active implementation target.** Keep one active target and at most one active implementation pull request per product lane.
3. **Event-first automation.** Pull-request events are the normal path. Schedules are recovery paths, not polling loops.
4. **Cheap checks first.** Run policy, scope and documentation checks on Linux. Use macOS or other scarce runners only for relevant platform paths.
5. **Limits become states.** A queued runner is `WAITING_RUNNER`; a 403 or 429 is `WAITING_API`; neither state justifies a no-op commit.
6. **Exact-head evidence.** Technical evidence belongs to the current pull-request head only.
7. **Small write surface.** Connector mutations are serial, scoped and followed by readback.
8. **Technical gates do not replace review.** Green checks are evidence, not semantic approval or merge authorization.

## Files to copy

```text
.agentic/repo-policy.json
.github/workflows/resource-aware-gate.yml
AGENTS.md
docs/CANARY_PROTOCOL.md
```

The policy file can be validated against:

```text
schemas/resource-aware-repo-policy-v1.schema.json
```

## Recommended operating flow

```text
Issue or verified target
→ one Draft PR
→ cheap exact-head checks
→ scarce platform checks only when applicable
→ semantic review
→ stable-head Ready transition
→ expected-head merge
→ terminal-state readback
```

## Resource-state interpretation

| Observation | State | Allowed response |
| --- | --- | --- |
| Required job queued or running | `WAITING_RUNNER` | Preserve head; wait for event or recovery cadence |
| API returns 403 or 429 | `WAITING_API` | Stop calls; respect retry/reset guidance |
| Required current-head check fails | `FIX_NEEDED` | Inspect only the failing step or log; apply smallest fix |
| Required checks succeed | `REVIEW_PENDING` | Perform semantic scope and risk review |
| Review succeeds | `CLOSER_PENDING` | Re-read head, checks and threads before merge |
| Pull request is merged or target closed | `COMPLETE` | Re-read terminal state and clear active target |

## Adoption order

1. Copy the files into a sandbox repository.
2. Run every canary in `docs/CANARY_PROTOCOL.md`.
3. Keep the gate read-only until the canaries are green.
4. Add a real product only after the stale-head, queued-runner and duplicate-comment cases are proven.
5. Add local or hosted AI producers later; keep merge authority separate.

## Deliberate omissions

This starter kit does not:

- create a permanent multi-agent runtime
- require a private memory repository
- assume scheduled LLM tasks are available
- assume unlimited GitHub API or runner capacity
- grant workflow merge permission
- add cross-repository credentials
- execute untrusted pull-request code in a privileged job

It is intentionally small enough to audit and extend.