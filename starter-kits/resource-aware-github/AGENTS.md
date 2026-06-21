# Agent Contract

This repository uses a small role-separated operating model. Roles are capabilities, not permanent bots.

## Shared rules

Every role must:

1. read current GitHub source before acting;
2. confirm repository, target, state and current head;
3. stay within the named files and stop rules;
4. treat queued runners and API limits as resource states;
5. avoid duplicate comments, retries and no-op commits;
6. perform at most one authorized mutation per cycle;
7. re-read the changed resource after every mutation;
8. report only observed evidence.

## Observer

Allowed:

- repository metadata
- files and commits
- issues and pull requests
- changed files and diffs
- checks, workflow summaries, comments, reviews and threads

Not allowed:

- file writes
- comments
- branch changes
- merges
- settings or secrets

## Planner

Allowed:

- select exactly one source-backed target when no implementation pull request is active
- define goal, allowed files, acceptance criteria, validation and stop rules
- classify owner-only boundaries

Not allowed:

- implement
- merge
- create parallel targets
- convert a waiting runner into a code defect

## Producer

Allowed:

- work on the single authorized target
- update one existing branch or create one narrow Draft PR
- make at most one product mutation before readback
- route a concrete latest-head failure back to review

Not allowed:

- merge
- force-reset branches to retrigger CI
- create timestamp-only or no-op commits
- run multiple writers on one branch
- claim unobserved validation

## Validation Watcher

Allowed:

- read current-head workflow summaries once
- classify `WAITING_RUNNER`, `WAITING_API`, `FIX_NEEDED` or runner complete
- fetch detailed steps or logs only for a concrete current-head failure

Not allowed:

- implement
- retry successful or merely queued jobs
- post repetitive status comments
- authorize merge

## Reviewer

Allowed:

- independently inspect scope, semantics, current-head checks, comments, reviews and threads
- decide `READY_FOR_CLOSE`, `FIX_NEEDED`, `WAITING_RUNNER`, `WAITING_API` or `BLOCKED_OWNER`

Not allowed:

- implement
- merge
- accept technical green as semantic approval
- use old-head evidence

## Closer

Allowed only after explicit reviewer authorization:

1. read the live target;
2. confirm current head and exact scope;
3. confirm required checks and review-thread state;
4. mark a Draft PR Ready;
5. re-read the unchanged head and evidence;
6. merge with the expected head;
7. verify terminal state.

Not allowed:

- merge a Draft directly
- implement fixes
- merge when the head changed
- merge more than one PR per cycle

## Recovery states

```text
WAITING_RUNNER  preserve the head; wait for event or recovery cadence
WAITING_API     stop connector calls and respect retry/reset guidance
FIX_NEEDED      inspect the exact failing evidence and route one small repair
BLOCKED_OWNER   preserve evidence and select no unsafe workaround
COMPLETE        verify terminal state before selecting another target
```

## Minimum evidence envelope

```text
TARGET_REPO
TARGET_KIND
TARGET_NUMBER
TARGET_STATE
TARGET_HEAD
CHANGED_FILES
WORKFLOW_RESULTS
COMMENTS_REVIEWS_THREADS
DRAFT_STATE
MERGEABILITY
EVIDENCE_SOURCE
NEXT_ALLOWED_ROLE
```
