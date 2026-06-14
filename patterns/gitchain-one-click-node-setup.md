# GitChain One-Click Node Setup Pattern

Status: public-safe proof-of-concept pattern.

This pattern describes the smallest setup that lets any public GitHub repository participate as a GitChain node without exposing private messages.

## Goal

A user with a GitHub repository should be able to join by adding a small public-safe folder:

```text
gitchain/
  node.json
  wallet.json
  commitments/
    README.md
  blocks/
    README.md
```

The repository may later add a GitHub Action validator and a GitHub Pages explorer, but neither is required for v0.

## One-click target

The future one-click version should be a GitHub template repository or GitHub App that creates:

```text
1. node manifest
2. wallet manifest
3. public-safe commitment folder
4. public-safe block folder
5. optional inbox issue
6. optional validator workflow
7. optional Pages explorer
```

## Manual v0 setup

### Step 1: Add node manifest

Copy `examples/gitchain-node-manifest-v0.json` into your repository as:

```text
gitchain/node.json
```

Update only public fields:

```text
node_id
operator
wallet_id
inbox
ledger_path
public endpoints
```

### Step 2: Add wallet manifest

Copy `examples/gitchain-wallet-v0.json` into:

```text
gitchain/wallet.json
```

The wallet is not financial and must not contain private keys.

### Step 3: Publish public commitments only

A private system may create a salted hash from a private message. Only the resulting commitment hash goes into the public repository.

```text
private_message + private_salt -> sha256 -> public_commitment_hash
```

Never publish the private message or salt.

### Step 4: Submit a block candidate

A block producer reads public commitments and proposes a cycle block by pull request.

The pull request should contain only public-safe artifacts.

### Step 5: Earn non-transferable reputation

If the contribution is accepted, a reputation event may be added.

Reputation is:

```text
non-transferable
non-financial
public contribution memory
not a token sale
not a payment promise
```

## GitHub resources used

```text
repository -> node identity
files -> manifests, commitments, blocks
pull request -> block proposal
review -> validation gate
commit -> auditable state transition
fork -> mirror node
pages -> optional explorer
workflow -> optional validator
issue -> optional public-safe inbox
reaction -> optional acknowledgement
```

## Public-safety requirements

Reject any setup or block candidate that includes:

```text
private messages
private salts
secrets
credentials
private project state
private issue or pull request details
raw logs
personal data
customer data
unredacted repository dumps
```

## What is needed to make this live

For a real public MVP, create a dedicated public registry repository with:

```text
README.md
CONTRIBUTING.md
SECURITY.md
patterns/
examples/
schemas/
registry/nodes/
registry/wallets/
blocks/
validators/
docs/quickstart.md
```

Keep private messages, salts, and private keys outside the registry.

## Recommended next step

Use the current playbook examples as the template for a dedicated public MVP repository only after the format is reviewed and stable.
