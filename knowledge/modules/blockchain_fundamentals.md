# Blockchain Fundamentals - Specialist Knowledge Module

**Domain:** Distributed systems, consensus, cryptography
**Load when:** Discussing blockchain concepts, consensus mechanisms, or distributed systems
**Version:** 1.0 (Wake 65)

---

## Core Concepts

### 1. Blockchain Basics

**Definition:** A distributed, immutable ledger of transactions organized into blocks linked by cryptographic hashes.

**Key Properties:**
- **Immutability** - Past blocks cannot be changed without breaking chain
- **Transparency** - All participants can verify the chain
- **Decentralization** - No single point of control
- **Consensus** - Agreement on state without central authority

### 2. Consensus Mechanisms

**Proof of Work (PoW):**
- Miners solve computational puzzles
- First to solve gets to add block
- Security through computational cost
- Examples: Bitcoin, early Ethereum

**Proof of Stake (PoS):**
- Validators stake tokens
- Selected to propose blocks based on stake
- Security through economic stake
- Examples: Ethereum 2.0, Cardano

**Byzantine Fault Tolerance (BFT):**
- Validators vote on blocks
- Requires 2/3+ agreement
- Fast finality
- Examples: Tendermint, Cosmos

### 3. Transaction Model

**UTXO (Unspent Transaction Output):**
- Transactions consume inputs, create outputs
- Each output can be spent once
- Parallel transaction processing
- Example: Bitcoin

**Account Model:**
- Accounts have balances
- Transactions modify balances
- Simpler mental model
- Example: Ethereum

### 4. Smart Contracts

**Definition:** Self-executing code on blockchain

**Properties:**
- Deterministic execution
- Transparent logic
- Immutable once deployed
- Composable (DeFi)

**Execution Models:**
- **EVM (Ethereum Virtual Machine)** - Stack-based, gas metered
- **WASM** - WebAssembly for blockchain
- **eBPF** - Extended Berkeley Packet Filter (Tockchain uses this)

### 5. State Management

**State Transitions:**
```
State(N) + Transaction → State(N+1)
```

**State Storage:**
- **On-chain** - Expensive, permanent
- **Off-chain** - Cheap, requires trust/proofs
- **Hybrid** - Commitments on-chain, data off-chain

**State Bloat:**
- Problem: State grows forever
- Solutions: State rent, pruning, expiry
- Tradeoff: Decentralization vs. scalability

### 6. Cryptographic Primitives

**Hash Functions:**
- SHA-256 (Bitcoin)
- Keccak-256 (Ethereum)
- Properties: Collision-resistant, one-way, deterministic

**Digital Signatures:**
- ECDSA (secp256k1) - Bitcoin, Ethereum
- EdDSA (ed25519) - Modern alternative
- Purpose: Prove ownership, authorize transactions

**Merkle Trees:**
- Hash tree structure
- Efficient proofs of inclusion
- Used for: Transaction trees, state trees

---

## Scalability Approaches

### Layer 1 (On-Chain)

**Sharding:**
- Split chain into parallel shards
- Each shard processes subset of transactions
- Challenge: Cross-shard communication

**Bigger Blocks:**
- More transactions per block
- Tradeoff: Centralization (bigger nodes)

**Faster Blocks:**
- Reduce block time
- Tradeoff: More orphans, less security

### Layer 2 (Off-Chain)

**State Channels:**
- Open channel, transact off-chain, close on-chain
- Example: Lightning Network

**Rollups:**
- Execute off-chain, post commitments on-chain
- Optimistic: Fraud proofs
- ZK: Validity proofs

**Sidechains:**
- Separate chain, pegged to main chain
- Own consensus, own security

---

## Economic Models

### Gas/Fees

**Purpose:**
- Prevent spam (DoS protection)
- Compensate validators
- Resource allocation

**Design Choices:**
- Fixed vs. dynamic pricing
- Fee markets vs. fixed fees
- Who pays: sender, recipient, protocol

### Tokenomics

**Supply Models:**
- Fixed supply (Bitcoin: 21M)
- Inflationary (Ethereum: ~2% annual)
- Deflationary (burn mechanisms)

**Utility:**
- Payment (medium of exchange)
- Staking (security)
- Governance (voting)
- Gas (computation)

---

## Security Considerations

### Attack Vectors

**51% Attack:**
- Control majority of hash power/stake
- Can rewrite recent history
- Mitigation: High cost, finality gadgets

**Double Spend:**
- Spend same coins twice
- Prevented by: Consensus, confirmations

**Front-Running:**
- See pending transaction, submit higher fee
- Common in DeFi
- Mitigation: Private mempools, commit-reveal

**Reentrancy:**
- Call back into contract mid-execution
- Famous: The DAO hack
- Mitigation: Checks-effects-interactions pattern

### Best Practices

1. **Deterministic Execution** - No randomness, no time dependencies
2. **Gas Limits** - Bound computation
3. **Access Control** - Who can call what
4. **Upgrade Patterns** - How to fix bugs
5. **Economic Security** - Attacks must be expensive

---

## DeFi Primitives

### Automated Market Makers (AMMs)

**Constant Product:** x * y = k
- Uniswap model
- No order book
- Liquidity pools

**Concentrated Liquidity:**
- Uniswap V3
- Capital efficiency
- More complex

### Lending Protocols

**Collateralized Lending:**
- Deposit collateral
- Borrow against it
- Liquidation if under-collateralized

**Flash Loans:**
- Borrow without collateral
- Must repay in same transaction
- Enables arbitrage, attacks

### Derivatives

**Perpetual Futures:**
- No expiry
- Funding rate mechanism
- Popular in crypto

**Options:**
- Right but not obligation
- Complex pricing
- Less common on-chain

---

## Consensus Deep Dive

### Finality

**Probabilistic Finality:**
- More confirmations = more secure
- Never 100% certain
- Example: Bitcoin (6 confirmations ~1 hour)

**Absolute Finality:**
- Once finalized, cannot revert
- Requires BFT consensus
- Example: Tendermint (instant finality)

### Liveness vs. Safety

**Liveness:** System keeps making progress
**Safety:** System never produces wrong result

**CAP Theorem:** Can't have all three:
- Consistency
- Availability  
- Partition tolerance

Blockchains choose: Consistency + Partition tolerance → Sacrifice availability during network splits

---

## Performance Metrics

**Throughput:** Transactions per second (TPS)
- Bitcoin: ~7 TPS
- Ethereum: ~15 TPS
- Solana: ~3000 TPS (claimed)

**Latency:** Time to finality
- Bitcoin: ~60 minutes (6 blocks)
- Ethereum: ~15 minutes (post-merge)
- BFT chains: Seconds

**Decentralization:** Node count, distribution
- More nodes = more decentralized
- Tradeoff with performance

---

## Common Patterns

### Commit-Reveal

1. User commits hash(value + nonce)
2. Wait for commitment period
3. User reveals value + nonce
4. System verifies hash matches

**Use:** Prevent front-running, fair ordering

### Time-Locked Contracts

- Funds locked until time T
- Enables: Vesting, escrow, atomic swaps

### Multi-Signature

- Require M of N signatures
- Use: Governance, security

### Proxy Patterns

- Separate logic from storage
- Enables upgrades
- Tradeoff: Complexity, trust

---

## Interoperability

### Cross-Chain Communication

**Bridges:**
- Lock on Chain A
- Mint on Chain B
- Trust model varies

**Atomic Swaps:**
- Hash time-locked contracts
- Trustless exchange
- Limited functionality

**Relays:**
- Light client verification
- Expensive on-chain
- Enables true interop

---

## Tockchain Context

Tockchain's design choices:
- **eBPF execution** - Proven, safe, efficient
- **Gas metering** - Economic DoS protection
- **Reactive triggers** - Efficient computation model
- **Dataflow paradigm** - Composable programs
- **Deterministic** - Consensus-safe

These choices reflect deep understanding of blockchain fundamentals and pragmatic engineering.

---

**Load this module when:**
- Discussing blockchain concepts with ct or Opus
- Explaining Tockchain design decisions
- Comparing different blockchain architectures
- Evaluating security or scalability approaches
