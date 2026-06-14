# GitChain Public Node

Status: public-safe v0 node scaffold.

This folder is the live public GitChain node area for `pokekarten/agentic-dev-playbook`.

It is a Git-backed public ledger surface for public-safe agent coordination artifacts.

## Current node files

```text
gitchain/
  node.json
  wallet.json
  commitments/
    README.md
  blocks/
    000000-genesis.json
```

## Allowed content

Only public-safe hashes, block files, node manifests, wallet manifests, validation notes, and non-transferable reputation events may be published here.

Private content, raw logs, raw chats, and project-internal live state must stay out of this folder.

## Chain rule

Each accepted block must link to the previous accepted block hash. The genesis block starts the public node timeline.

## Next implementation step

Use `scripts/validate_gitchain.py` before accepting future GitChain changes.
