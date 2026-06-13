# Privacy Before Publishing

## Purpose

Before writing to a public repository, check whether the content is safe to publish.

Public repositories should contain reusable patterns, not private project memory.

## Checklist

Public content must be:

- generic enough to be useful outside one private project
- free of private repository names unless intentionally public examples
- free of private pull request numbers, branch names and commit hashes
- free of internal blocker histories and incident details
- free of raw chat text
- free of secrets, tokens, environment values and credentials
- free of personal data and customer data
- free of proprietary data dumps

## Rewrite pattern

Convert concrete internal detail into a generic rule.

```text
Bad public form:
In private project X, branch Y failed because of internal blocker Z.

Good public form:
When repository status is uncertain, verify repository inventory and evidence before reporting status.
```

## Routing rule

```text
Concrete private fact -> private memory
Generic reusable rule -> public playbook
Abstract decision example -> evaluation lab
Raw transcript / sensitive detail -> do not store
```

## Final question

Before publishing, ask:

```text
Would this text still be safe and useful if read by someone outside the project?
```

If the answer is not clearly yes, do not publish it publicly.
