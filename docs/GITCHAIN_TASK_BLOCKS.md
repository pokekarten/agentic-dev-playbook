# GitChain Task Blocks

Last updated: 2026-06-14

## Purpose

Improve the GitChain model so every scheduled agent task can become its own public-safe task block.

The previous model used one public cycle block for the full ten-slot hour. The improved model uses two layers:

```text
Task Block  = one public-safe block per scheduled slot
Cycle Block = one hourly summary block that references the ten task block hashes
```

## Why this is better

One block per task gives:

```text
clearer provenance
smaller audit units
slot-level hashes
better replay checks
better public metrics
cleaner later token/reputation accounting
```

The cycle block still matters. It links the ten task blocks into one hourly checkpoint.

## Ten task blocks per cycle

```text
slot00 -> task block 00
slot06 -> task block 06
slot12 -> task block 12
slot18 -> task block 18
slot24 -> task block 24
slot30 -> task block 30
slot36 -> task block 36
slot42 -> task block 42
slot48 -> task block 48
slot54 -> task block 54 and optional cycle block
```

## Task block fields

A task block should contain only public-safe data:

```text
kind: TASK_BLOCK
version: v0
cycle_id: YYYYMMDD-HH
slot: slot00..slot54
minute: 02..56
task: short public-safe role name
result_state: planned | observed | done | skipped | blocked
public_summary: short sanitized summary
candidate_type: none | note | metric | schema_example | block_candidate
evidence_hash: hash only, not private evidence
previous_task_hash: previous task block hash or null
task_hash: hash of this public task block
timestamp: ISO-like timestamp
public_safety: public-safe | redacted
```

## Chain shape

```text
genesis block
  -> slot00 task block
  -> slot06 task block
  -> slot12 task block
  -> slot18 task block
  -> slot24 task block
  -> slot30 task block
  -> slot36 task block
  -> slot42 task block
  -> slot48 task block
  -> slot54 task block
  -> hourly cycle block
```

## Cycle block shape

The cycle block should not repeat private details. It should reference the task blocks:

```text
kind: AGENT_BLOCK
height: cycle number
previous block hash
task_block_hashes: ten hashes
message_root: root over the ten task hashes
public_summary: sanitized cycle-level summary
attestations: public-safe attestations only
```

## Public safety

Task blocks must not contain:

```text
secrets
credentials
private project state
active private PR details
raw logs
raw chats
personal data
customer data
private issue links
unverified completion claims
```

If a slot has only private information, its public task block should say:

```text
result_state: observed
candidate_type: none
public_summary: private result observed; no public-safe detail emitted
```

## Incentive model later

Task blocks make incentives easier:

```text
+ reputation for valid task block
+ reputation for valid cycle block
+ reputation for mirroring task block hashes
+ reputation for schema validation
- penalty for spam
- penalty for private data leaks
- penalty for false attestations
```

Do not add a tradable token until the task-block model has been tested with real public-safe cycles.

## Slot54 role

Slot54 may create:

```text
one task block for slot54
one cycle block referencing all ten task block hashes
```

Only if the cycle is reconstructable and public-safe.

If not safe, Slot54 should skip the public block and write only a private health note.
