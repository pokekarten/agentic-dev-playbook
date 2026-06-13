# Manifest Plus Validator

For data growth, start with a small manifest and a validator hook before adding large data batches.

## Pattern

```text
1. Create a small manifest that states scope and source policy.
2. Add a validator that checks the manifest against existing local data.
3. Add larger data only in later reviewed slices.
```

## Benefit

This keeps data changes small, reviewable and easy to roll back.
