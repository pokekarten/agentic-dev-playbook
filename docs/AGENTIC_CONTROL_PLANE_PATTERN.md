# Agentic Control Plane Pattern

Last updated: 2026-06-14

## Purpose

This public-safe pattern describes how to use a GitHub repository as a control plane for scheduled AI-agent work without exposing private project state.

## Pattern

Use three layers:

1. **Control plane repository**: stores the generic operating contract, slot registry, score policy, handoff rules, and safety rules.
2. **Runner layer**: scheduled assistants or external runners read the control plane, perform one narrow role, and produce a structured result.
3. **Work repositories**: project repositories store the actual issue, PR, task, validation, and implementation truth.

## Core rule

Agents are roles, not repositories. A multi-agent system should not create one repository per agent by default. Use repositories as responsibility boundaries and agents as scheduled or triggered roles.

## Required run contract

Each run should end with a compact result block:

```text
BOT_RESULT:
slot:
repo_scope:
read_sources:
collision_check:
action_taken:
terminal_result:
progress_score: 0-3
evidence_score: 0-3
risk_score: 0-3
learning_candidate: yes/no
learning_destination:
next_handoff:
self_improvement_note:
```

## Progress scoring

```text
0 = no-op/status only
1 = next target/blocker clarified
2 = useful issue/PR/file/control update
3 = PR opened/merged or meaningful product/user-visible progress
```

## Safety rules

- Read current sources before writing.
- Do not let memory override source evidence.
- Check for file, issue, PR, branch, and head-SHA collisions before mutating.
- Use comments or issues for append-only run logs; avoid many agents appending to the same file.
- Keep private project details out of public playbooks.
- Store only durable, sanitized, reusable patterns publicly.

## Self-improvement loop

```text
Run -> BOT_RESULT -> aggregate scores -> identify repeated failures -> update control rule or prompt only when evidence is repeated or source-backed.
```

Do not treat a single weak signal as permission to rewrite the system.
