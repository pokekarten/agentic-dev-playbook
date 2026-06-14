# WIP-limited progress loop

## Purpose

Use this pattern when AI-assisted repository work starts creating too many status checks, review loops, side tasks or process documents without enough product progress.

The goal is to keep work source-driven, small and finishable.

## Default loop

```text
1. Read the repository's current task file.
2. Pick exactly one work item.
3. Classify it as product, safety, validation, cleanup or learning.
4. Define the smallest terminal result before changing anything.
5. Do the smallest safe action.
6. Re-read the changed source.
7. Report evidence, risks and the next smallest step.
```

## WIP limit

Keep at most one active work item per repository context.

Do not open a second task for the same repository until the current item has one terminal result:

```text
MERGED
CLOSED
PR_OPENED
FILE_CHANGED
ISSUE_UPDATED
PATCH_READY
NEXT_UNBLOCKED_TASK_SELECTED
NO_CHANGE_VERIFIED
```

## Progress priority

Prefer this order:

1. Product or user-visible progress.
2. Safety or privacy fix.
3. Validation evidence that unblocks product work.
4. Cleanup of stale blockers.
5. Public playbook or learning capture.

Do not create process documentation when a safe product step is available.

## Evidence rule

Report each claim with an evidence tier:

```text
verified_source
connector_read
ci_or_check_log
local_run
user_provided
memory_only
assumption
```

Never turn `memory_only` or `assumption` into status truth.

## Stop rules

Stop and report instead of continuing when:

- the next action would mix two project contexts,
- the task would require secrets, private data or raw logs,
- validation is required but no current evidence exists,
- the change would expand scope beyond the current task file,
- the work is becoming another process layer instead of finishing an item.

## Good final output

```text
Status:
Work item:
Terminal result:
Evidence:
Files changed:
Risks:
Next smallest step:
```
