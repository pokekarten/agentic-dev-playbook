# GitHub Connector Operator Pattern

## Purpose

Use a GitHub connector as a small repository operator, not just as a status reporter.

This pattern is for AI-assisted repository work where the assistant can read repository sources, inspect pull requests, update small files, create issues or pull requests, and possibly merge when explicit gates pass.

## Boundary

A connector is not a local shell.

It can usually inspect repository state and perform API-backed repository actions. It must not claim local command execution unless a local runtime, CI log, or user-provided evidence actually proves it.

## Operating loop

```text
Read gate -> scope gate -> evidence gate -> action gate -> re-check gate
```

### 1. Read gate

Use direct read-only evidence first:

- repository metadata
- file contents
- issue body and acceptance criteria
- pull request metadata
- changed file list
- patch or diff
- commit status, workflow runs, logs, or artifacts when available

Avoid indirect evidence when direct evidence exists. Do not probe capabilities by performing write actions.

### 2. Scope gate

Before changing or merging anything, compare the requested task with:

- allowed repository
- allowed branch/base
- allowed files
- explicit stop rules
- privacy boundary
- expected head SHA when reviewing a pull request

If the changed files exceed scope, stop or request changes.

### 3. Evidence gate

Separate evidence types clearly:

```text
verified_by_connector_read
claimed_in_pr_body
visible_in_ci_or_status
not_executed_here
owner_input_required
```

Never convert missing local command execution into a passed test claim.

### 4. Action gate

Use the smallest safe action:

- comment with exact missing evidence
- request changes
- update one small file with the current file SHA
- create a focused issue
- create a draft pull request
- mark a draft ready only after scope review
- merge only after a current head SHA re-check

For file writes, work serially. For pull request merges, use the current head SHA as the expected SHA.

### 5. Re-check gate

After any write or state transition, re-read the relevant source:

- file content after update
- PR metadata after ready/merge transition
- issue state after close/update
- branch/head SHA after changes

Report only what was actually changed or verified.

## Good output format

```text
Status:
Evidence:
Changed files:
Risks:
Next smallest step:
```

## Anti-patterns

- reporting status without checking current source
- treating connector or CI gaps as automatic blockers
- claiming local checks without execution
- using mutation calls as capability tests
- mixing project contexts in one change
- writing process docs when product progress is available
- merging without a fresh head SHA check

## Generic example

A documentation-only pull request changes exactly the allowed documentation file and contains no runtime, workflow, dependency, secret, or lockfile changes. Local commands were not run, and no CI run is visible.

Decision:

```text
FOLLOW_UP or MERGE_CANDIDATE depending on the repository policy.
```

Reason:

The connector can verify scope and diff, but it cannot honestly claim local validation. If repository policy allows documentation-only merges without CI, proceed through the merge gate with a fresh head SHA. Otherwise comment with exact missing validation.
