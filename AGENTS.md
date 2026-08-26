# Agentic development playbook — agent guidance

## Progress-first execution default

This repository exists to improve practical agentic development, not to create process for its own sake.

- **ChatGPT with the live GitHub connector is the default contributor** for repository inspection, edits, reviews and coordination.
- **Use ChatGPT's Linux environment first** for tests, scripts, builds, data analysis and model/tool experiments that can run there.
- **Escalate to Mac/Codex only for the smallest host-specific slice** that truly requires macOS, a local-only runtime/asset, device behavior, signing, performance measurement or execution unavailable in Linux. Return to ChatGPT/GitHub after the result.
- Other agents may run in parallel only on disjoint work. Check live GitHub before starting and avoid duplicate implementation.
- Master prompts are reusable task templates, not mandatory workflow, scheduler or truth.
- Do not add a new controller, slot system, ledger, gate, status document or approval layer unless it solves a demonstrated failure or coordination problem.
- Prefer executable examples, tests, measurements and direct improvements over more workflow prose.
- Apply exact provenance/byte identity only when the claim genuinely depends on it; otherwise optimize technical correctness, current usefulness, maintainability and reproducible-enough tests.

Live GitHub state is the operational truth. Use the smallest coordination mechanism that lets work continue safely.
