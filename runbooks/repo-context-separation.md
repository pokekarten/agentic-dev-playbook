# Repository Context Separation

Start repository work by naming the active context.

## Required header

```text
Repo context:
GitHub path:
Task:
Allowed scope:
Must not mix with:
```

## Rule

Work in one repository context at a time. Before changing files, reviewing a pull request, or reporting status, name the repository and allowed scope.

Current repository source owns current implementation, issue, pull-request, branch, CI and validation truth. Do not copy volatile state into a cross-project memory or playbook just to make it easier to find.

## Canonical-home rule

Give each durable fact one canonical home.

```text
project-specific implementation, evidence or decision -> owning project repository
private durable cross-project routing or lesson       -> private memory/router
public reusable method                                -> public playbook after sanitization
abstract or synthetic decision example                -> evaluation/training lab after redaction
volatile, noisy or sensitive material                 -> do not centralize
```

Links and short pointers may exist elsewhere, but they must not become a second independently editable truth.

## Learn after progress

Do the project work first. At the end of a meaningful cycle, ask whether anything remains useful beyond that project.

Promote only the reusable residue. Do not create a new framework, control plane, slot system or document family merely to preserve a lesson. If an existing canonical surface can hold the lesson, update it instead.

Consistency across repositories means consistent authority and evidence semantics, not identical repository structure or workflow.

## Handoff

End meaningful sessions with:

```text
Repo:
Done:
Current blocker:
Next smallest step:
Learning / no new rule needed:
```
