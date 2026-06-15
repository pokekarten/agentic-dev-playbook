# Public-safe hash-chain examples

This directory contains public-safe demo assets for the GitHub-native Agent Control Pattern.

## What is included

```text
validate_candidate_envelope.py   Read-only validator for demo candidate envelopes.
generate_demo_fixtures.py        Generates positive and negative demo fixtures during workflow runs.
```

The fixtures are generated at workflow runtime under `validation-output/generated-fixtures/` so hash-bearing test data does not drift from the validator implementation.

## What is intentionally not included

```text
private project truth
private repository names
active PR or CI state
secrets
automatic write actions
scheduled workflow triggers
```

## Manual workflow

The public workflow is:

```text
.github/workflows/public-agent-control-validation.yml
```

It is `workflow_dispatch` only, read-only, non-parallel, and uses public-safe generated fixtures.

## Expected result

```text
valid.json -> pass
no_block.json -> pass
reject_hash_only.json -> fail intentionally
reject_bad_hash.json -> fail intentionally
```

If a negative fixture passes, the validator is too weak.
