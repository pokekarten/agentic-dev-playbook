# Execution honesty before status

## Purpose

Status reports should describe only work that was actually checked or changed.

This prevents agentic workflows from turning recommendations, missing validation, failed tool paths or skipped actions into apparent progress.

## Rule

Before reporting progress, separate four states:

```text
Checked: evidence was read or verified.
Changed: a file, issue, pull request or setting was actually updated.
Recommended: a next action was chosen but not executed.
Blocked or limited: execution could not continue, and the reason is explicit.
```

Never label a recommendation, skipped action or unavailable check as completed work.

## Repetition-loop guard

If the same recommendation appears again without new evidence:

1. Re-check whether the prior issue, pull request or task already completed it.
2. If safe, take the smallest concrete action.
3. If execution is not available, provide the exact patch, prompt or handoff.
4. If the recommendation is stale, replace it with the current next step.

## Public-safe reporting pattern

Use neutral wording:

```text
Status: no files changed.
Checked: source A and source B.
Recommendation: next smallest safe step is X.
Limit: Y was not executed because Z.
Risk: low / medium / high, with reason.
```

Do not include private repository names, private issue numbers, internal blocker histories, secrets, environment values, raw chat text or customer data in examples.

## Decision pattern

- If it was not checked, say it was not checked.
- If it was not changed, say no change was made.
- If a tool path failed, state the failed path and switch to a safer source or exact handoff.
- If a child task has completed, do not repeat the parent recommendation without updating the next step.
