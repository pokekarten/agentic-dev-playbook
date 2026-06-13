# Pull Request Gate

## Purpose

Use a pull request gate before marking a change ready or merging it.

The gate should protect scope, validation quality and repository context without turning small work into a process loop.

## Required checks

1. Confirm the active repository context.
2. Confirm the pull request state and base branch.
3. Confirm the changed files match the task scope.
4. Confirm no unrelated files, secrets, generated dumps or environment files are included.
5. Confirm validation evidence is present or explicitly missing.
6. Confirm unresolved review comments or blocker notes are addressed.
7. Confirm the final decision uses the latest reviewed head SHA when relevant.

## Decision outcomes

```text
APPROVE: scope is clean and required evidence is present.
FOLLOW_UP: scope looks safe, but validation or review evidence is missing.
REQUEST_CHANGES: scope, privacy or correctness issue is present.
BLOCKED: no safe progress is possible without owner input or external fix.
```

## Public-safe example

```text
A small pull request changes one validator and one documentation file.
The files match the stated task.
Validation evidence is not available yet.
Decision: FOLLOW_UP, not merge-ready.
```

## Privacy rule

Do not publish private repository names, private pull request numbers, internal branch names, blocker histories, raw chat text, secrets, environment values or customer data in public gate examples.
