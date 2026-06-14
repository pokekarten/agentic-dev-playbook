# Ten-Slot GitChain Cycle

Last updated: 2026-06-14

## Purpose

Describe how ten hourly agent tasks can each become one public-safe task block and then produce one public-safe hourly GitChain cycle block without leaking private project truth.

## Schedule

A full cycle starts at minute 02 and then runs every six minutes.

```text
slot00  minute 02  coordinate runway
slot06  minute 08  scan iGentic source
slot12  minute 14  gate iGentic PRs
slot18  minute 20  advance iGentic micro-step
slot24  minute 26  scan Pokekartenkiste source
slot30  minute 32  gate Pokekartenkiste PRs
slot36  minute 38  advance Pokekartenkiste micro-step
slot42  minute 44  curate abstract learning
slot48  minute 50  improve public playbook
slot54  minute 56  align Brain state and decide public-safe blocks
```

## Block model

The improved model has two layers:

```text
TASK_BLOCK  = one public-safe block per scheduled slot
CYCLE_BLOCK = one hourly block that references the ten task block hashes
```

This means every task can be hashed independently.

```text
slot00 -> TASK_BLOCK hash
slot06 -> TASK_BLOCK hash
slot12 -> TASK_BLOCK hash
slot18 -> TASK_BLOCK hash
slot24 -> TASK_BLOCK hash
slot30 -> TASK_BLOCK hash
slot36 -> TASK_BLOCK hash
slot42 -> TASK_BLOCK hash
slot48 -> TASK_BLOCK hash
slot54 -> TASK_BLOCK hash
all ten hashes -> CYCLE_BLOCK message_root
```

## Rule

Project slots keep doing project work.

They should not publish private details into public GitChain files.

Each slot may produce a public-safe candidate signal inside its normal BOT_RESULT:

```text
gitchain_candidate: none | public_safe_note | public_safe_metric | public_safe_schema_example | public_safe_block_candidate
```

Slot54 is the only slot that may propose or create public-safe task blocks or a public-safe cycle block after checking:

```text
no secrets
no private project truth
no active private PR details
no raw logs
no raw chats
no personal data
no unverified claims
```

## Private to public conversion

```text
private BOT_RESULTs from ten slots
-> Slot54 health review
-> sanitized task summaries
-> up to ten public TASK_BLOCK files
-> one optional public CYCLE_BLOCK file
```

## Task block content

A public task block should contain only generic public-safe data:

```text
cycle id
slot id
slot minute
task title
result state
public summary
candidate type
evidence hash only
task hash
previous task hash
timestamp
public-safety attestation
```

## Cycle block content

A public cycle block should contain only generic metrics and hashes.

Allowed:

```text
cycle id
slot schedule
slot count
ten task block hashes
public-safe learning summary
schema version
previous public block hash
message root over task hashes
attestations
```

Not allowed:

```text
private project names when not already public-safe
private issue links
active PR gate truth
raw logs
private decisions
secrets
personal data
```

## Example cycle flow

```text
20:02 slot00 coordinates -> task block candidate
20:08 slot06 scans iGentic -> task block candidate
20:14 slot12 gates iGentic -> task block candidate
20:20 slot18 advances iGentic -> task block candidate
20:26 slot24 scans Pokekartenkiste -> task block candidate
20:32 slot30 gates Pokekartenkiste -> task block candidate
20:38 slot36 advances Pokekartenkiste -> task block candidate
20:44 slot42 extracts abstract learning -> task block candidate
20:50 slot48 updates public-safe docs if needed -> task block candidate
20:56 slot54 checks evidence -> may write task blocks and one cycle block
```

## Stop rule

If the cycle is not reconstructable, contains private detail, or creates noise, Slot54 must not write public blocks. It should write a private health note instead.
