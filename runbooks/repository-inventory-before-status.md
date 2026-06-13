# Repository inventory before status

## Purpose

When a user asks about repository ownership, creation dates, recent activity or project status, do not answer from memory first.

Start with a read-only repository inventory, then interpret the result.

## Rule

Use this order:

1. Confirm the connected account or installation.
2. List accessible repositories by affiliation: owner, collaborator and organization member.
3. Separate public profile visibility from connector visibility.
4. Verify creation-date claims through repository metadata or date-filtered repository search.
5. Read project files only after the inventory is complete.
6. Separate verified source data from remembered project context.
7. State limitations when exact metadata is not exposed.

## Why

Project memory can know that a project exists, but it cannot prove when a repository was created.

A public profile can show public repositories, but it cannot show private repositories.

A connector can show private repositories when the authenticated user has access, but that access must still be verified before reporting.

## Public-safe reporting pattern

Use neutral wording:

```text
I found N accessible repositories for the connected account.
X are owned by the account.
Y are collaborator repositories.
Z are organization-member repositories.
Repository A matches the requested creation-date filter.
Repository B predates the requested date.
```

Do not include private repository names, internal branch names, private pull request numbers, blocker histories, raw chat text, secrets, environment values or customer data in public examples.

## Decision pattern

- If the question is about facts: inventory first.
- If the question is about process: inventory first, then explain the process gap.
- If memory conflicts with source data: source data wins.
- If metadata is incomplete: say which field is missing and which evidence was used instead.
