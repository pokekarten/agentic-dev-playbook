# agentic-dev-playbook

Open agentic development playbook for PR gates, repository workflows and safe progress patterns.

## Purpose

This repository contains public, reusable playbooks for small agentic software-development workflows.

The goal is to make AI-assisted project work safer and more repeatable by documenting generic patterns for:

- repository context separation
- repository inventory before status reporting
- execution honesty before progress reporting
- privacy checks before publishing public process knowledge
- pull request gate reviews
- small safe implementation slices
- debugging before declaring work blocked
- session handoffs
- data-growth controls such as manifest plus validator hooks
- connector-backed repository operations
- WIP-limited progress loops
- Git-backed public agent nodes
- low-noise agent messaging
- public-safe task and cycle records

## Privacy boundary

This repository is public.

Do not include:

- private repository names unless they are intentionally public examples
- private PR numbers, branch names or internal blocker histories
- secrets or environment values
- personal data
- raw private chat logs
- proprietary data dumps

Use sanitized, generic examples only.

## First playbooks

- `runbooks/repo-context-separation.md`
- `runbooks/repository-inventory-before-status.md`
- `runbooks/execution-honesty-before-status.md`
- `runbooks/privacy-before-publishing.md`
- `runbooks/pr-gate.md`
- `runbooks/debug-before-blocking.md`
- `runbooks/github-connector-operator.md`
- `runbooks/wip-limited-progress-loop.md`
- `patterns/five-line-handoff.md`
- `patterns/manifest-plus-validator.md`

## Public agent-node patterns

- `docs/AGENTIC_CONTROL_PLANE_PATTERN.md`
- `docs/AGENT_BUS_PUBLIC_NODE_CONCEPT.md`
- `docs/GITCHAIN_AGENT_MESSAGING.md`
- `docs/GITCHAIN_TASK_BLOCKS.md`
- `docs/TEN_SLOT_GITCHAIN_CYCLE.md`

## GitChain node MVP prototype

A public-safe proof-of-concept for GitHub-native nodes, private-message commitments, block producers, wallets, and non-transferable reputation.

Start here:

- `patterns/gitchain-private-commitment-prototype.md`
- `patterns/gitchain-one-click-node-setup.md`

Example artifacts:

- `examples/gitchain-commitment-v0.json`
- `examples/gitchain-wallet-v0.json`
- `examples/gitchain-wallet-balance-v0.json`
- `examples/gitchain-node-manifest-v0.json`
- `examples/gitchain-block-producer-v0.json`
- `examples/gitchain-cycle-block-v0.json`
- `examples/gitchain-reputation-event-v0.json`

Safety rule: this prototype publishes only public-safe hashes, manifests, examples, block candidates, and reputation events. Private messages, salts, private keys, private project state, secrets, and raw logs must stay out of this public repository.

## Public schemas and examples

- `schemas/gitchain-agent-message-v0.schema.json`
- `schemas/gitchain-agent-block-v0.schema.json`
- `examples/gitchain-task-block-v0.json`

## Reusable starter kits

- `starter-kits/resource-aware-github/README.md` — a copyable, Free-Tier-aware GitHub operating baseline
- `starter-kits/resource-aware-github/.agentic/repo-policy.json` — WIP, connector, Actions, evidence and merge policy
- `starter-kits/resource-aware-github/.github/workflows/resource-aware-gate.yml` — an always-reporting, read-only policy gate
- `starter-kits/resource-aware-github/AGENTS.md` — Observer, Planner, Producer, Watcher, Reviewer and Closer contracts
- `starter-kits/resource-aware-github/docs/CANARY_PROTOCOL.md` — sandbox tests for queues, API limits, stale heads and merge transactions
- `schemas/resource-aware-repo-policy-v1.schema.json` — reusable policy schema

## License

Apache-2.0
