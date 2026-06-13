# Debug Before Blocking

## Purpose

Do not declare repository work blocked just because the first check fails or the cause is unclear.

A blocker should mean that no safe progress remains after inspection, research and a smaller alternative have been considered.

## Rule

Before calling work blocked:

1. State the exact problem.
2. Check the local repository evidence available through the current tools.
3. Read the relevant project or workflow documentation.
4. Identify at least three plausible causes when the cause is unclear.
5. Pick the most likely cause.
6. Define the safest next test or inspection.
7. Try a smaller safe step if the original task cannot continue.
8. Report what is truly blocked and what can still move forward.

## Good blocker language

```text
Problem:
Likely cause:
Evidence:
Safe next test:
Unblocked smaller step:
Decision:
```

## Public-safe example

```text
A workflow check is unavailable.
Do not stop immediately.
Inspect the repository state, changed files and validation notes.
If the code diff is small and no sensitive files changed, continue with a manual review note and request missing validation evidence.
```

## Privacy rule

Use only generic examples in this public repo. Do not include private repository names, private branch names, private pull request numbers, internal incident histories, raw chat text, secrets, environment values or customer data.
