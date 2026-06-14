# Ten-Slot GitChain Cycle

Last updated: 2026-06-14

## Purpose

Describe how ten hourly agent tasks can produce one public-safe GitChain cycle block without leaking private project truth.

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
slot54  minute 56  align Brain state and decide public-safe cycle block
```

## Rule

Project slots keep doing project work.

They do not write public GitChain blocks directly.

Instead, each slot may produce a public-safe candidate signal inside its normal BOT_RESULT:

```text
gitchain_candidate: none | public_safe_note | public_safe_metric | public_safe_schema_example
```

Slot54 is the only slot that may propose or create a public-safe cycle block after checking:

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
-> sanitized cycle summary
-> optional public AGENT_BLOCK
```

## Cycle block content

A public cycle block should contain only generic metrics and hashes.

Allowed:

```text
cycle id
slot schedule
slot count
public-safe learning summary
schema version
previous public block hash
message root placeholder or computed hash
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
20:02 slot00 coordinates
20:08 slot06 scans iGentic
20:14 slot12 gates iGentic
20:20 slot18 advances iGentic
20:26 slot24 scans Pokekartenkiste
20:32 slot30 gates Pokekartenkiste
20:38 slot36 advances Pokekartenkiste
20:44 slot42 extracts abstract learning
20:50 slot48 updates public-safe docs if needed
20:56 slot54 checks evidence and may write one public-safe block
```

## Stop rule

If the cycle is not reconstructable, contains private detail, or creates noise, Slot54 must not write a public block. It should write a private health note instead.
