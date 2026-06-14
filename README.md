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

## Public schemas and examples

- `schemas/gitchain-agent-message-v0.schema.json`
- `schemas/gitchain-agent-block-v0.schema.json`
- `examples/gitchain-task-block-v0.json`

## License

Apache-2.0
