TXN v1.0 Architecture

Goal

TXN is a blockchain transaction analysis engine.

Its purpose is not simply downloading blockchain history.

Its purpose is to understand what happened in every blockchain transaction and export that information to tax software.

---

Pipeline

Fetch
    ↓
Merge
    ↓
Normalize
    ↓
Analyze
    ↓
Export

Every stage has exactly one responsibility.

---

Fetch

Input

Blockchain Explorer / API

Output

Raw blockchain records

Responsibilities

- Download transactions
- Download token transfers
- Download NFT transfers
- Download internal transactions

No tax logic.

No transaction classification.

---

Merge

Input

Multiple raw datasets.

Output

One combined dataset.

Responsibilities

- Merge explorer responses
- Remove duplicates
- Preserve all records

No tax logic.

---

Normalize

Input

Merged blockchain records.

Output

Normalized Transaction objects.

Responsibilities

- Convert explorer-specific fields into one common format.
- Group records belonging to the same blockchain transaction.
- Preserve every event.

No tax classification.

---

Transaction

One blockchain transaction becomes one Transaction object.

Example

Transaction

- hash
- chain
- wallet
- timestamp
- events[]

Events describe what actually happened.

Examples

- Native Transfer
- ERC20 Transfer
- ERC721 Transfer
- ERC1155 Transfer
- Internal Transfer
- Gas Fee

---

Analyze

Input

Transaction object.

Output

Transaction Type.

Examples

- SEND
- RECEIVE
- SELF_TRANSFER
- SWAP
- BRIDGE
- STAKE
- UNSTAKE
- REWARD
- AIRDROP
- LP_ADD
- LP_REMOVE
- NFT_MINT
- NFT_TRADE
- BORROW
- REPAY

Each analyzer has one responsibility.

If it cannot classify the transaction it returns None.

The engine executes analyzers from most specific to most generic.

---

Export

Exporters never inspect raw blockchain data.

They only consume normalized transactions.

Supported exporters

- Cryptact
- Koinly

Future

- CoinTracking
- CoinTracker
- TaxBit
- CSV
- JSON

---

Design Principles

Single Responsibility

Every module has exactly one purpose.

Chain Agnostic

Business logic must never depend on Ethereum, Somnia, TON or any specific chain.

Plugin Architecture

Adding a new chain requires only a new fetcher.

Adding a new tax platform requires only a new exporter.

Adding new transaction intelligence requires only a new analyzer.

No duplicated logic.

---

Long-Term Goal

TXN should become a reusable blockchain transaction engine capable of supporting multiple chains, multiple tax platforms and multiple analysis modules without changing the core pipeline.
