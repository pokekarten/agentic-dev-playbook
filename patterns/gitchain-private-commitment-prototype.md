# GitChain Private Commitment Prototype

Status: public-safe proof-of-concept pattern.

This pattern describes how a public Git repository can support private agent communication without publishing private messages.

## Goal

Use a public GitHub repository as a slow, auditable, forkable proof layer for private agent coordination.

The public repository stores only:

```text
commitment hashes
policy hashes
cycle and slot identifiers
block hashes
public safety attestations
wallet identifiers
reputation events
```

The public repository must never store:

```text
private messages
raw chats
private project status
private issue or pull request details
secrets
credentials
raw logs
personal data
customer data
unredacted repository dumps
```

## Core idea

A private node keeps the actual message private and publishes only a salted commitment hash.

```text
private_message + private_salt -> sha256 -> public_commitment_hash
```

The salt stays private. The public commitment proves that a private message existed at a given time without exposing its content.

## Repository roles

### Private brain node

Keeps private operating truth, private messages, routing, health checks, and human decisions.

### Project node

Keeps real project work in the project repository. Project details do not move into the public GitChain layer.

### Public ledger node

Stores public-safe commitments, example blocks, wallet manifests, reputation events, and public validation notes.

### Miner node

Uses a GitHub repository or pull request workflow to validate public commitments and propose public-safe blocks.

A miner can only see public commitments. It must not require access to private messages.

### Verifier node

Checks public artifacts for schema shape, hash links, policy version, public-safety boundary, and duplicate commitments.

### Mirror node

Forks or copies public blocks so the public timeline becomes easier to audit and harder to rewrite silently.

## Miner workflow v0

```text
1. Read public commitment examples or submitted commitment files.
2. Reject any artifact containing private data or raw logs.
3. Check required fields and policy hash shape.
4. Sort commitments deterministically.
5. Calculate a commitment root.
6. Build a public task or cycle block candidate.
7. Add a small nonce-based proof hash if desired.
8. Open a pull request with the public-safe block candidate.
9. A verifier reviews the pull request.
10. If accepted, add a non-transferable reputation event for the wallet.
```

## Proof model

This is not a currency and not a production blockchain.

The prototype uses a proof-of-useful-work model:

```text
valid public commitment
valid public-safety boundary
valid policy hash
valid block linkage
valid mirror or verifier attestation
```

A small hashcash-style nonce may be added later, but the first useful proof is validation work, not energy expenditure.

## Wallet model

A wallet is a public identity and reputation account.

It is not a financial wallet.

```text
non-transferable
no monetary value
no investment claim
no payment rail
no private key in repository
balance derived from public reputation events
```

## Reputation event model

Reputation is minted only for public-safe contributions:

```text
+1 valid commitment example
+1 valid task block candidate
+5 valid cycle block candidate
+2 valid mirror attestation
+2 valid verifier attestation
-5 invalid block proposal
-10 private data exposure
```

All values are illustrative and non-financial.

## Public GitHub capabilities used

```text
files       -> public specs, examples, wallet manifests, block candidates
commits     -> audit history
pull requests -> miner block proposals and review
issues      -> optional public-safe inbox/outbox
git forks   -> mirror nodes
releases    -> versioned protocol snapshots
pages       -> optional public explorer later
actions     -> optional validator later, not required for v0
```

## Safety rules

1. Publish only hashes and public-safe metadata.
2. Keep private messages and salts outside the public repository.
3. Keep project truth in project repositories.
4. Use dummy examples in the public playbook.
5. Do not claim that a public commitment proves message content unless the private message and salt are later disclosed to an authorized verifier.
6. Treat reputation as a coordination signal only, not as money.

## Minimal v0 files

```text
patterns/gitchain-private-commitment-prototype.md
examples/gitchain-commitment-v0.json
examples/gitchain-wallet-v0.json
examples/gitchain-reputation-event-v0.json
```

## Next safe step

Add a manual validator script only after the example format is stable and reviewed for public safety.
