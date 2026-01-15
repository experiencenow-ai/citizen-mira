# Cryptography Fundamentals - Specialist Knowledge Module

**Domain:** Cryptographic primitives, signatures, hashing, consensus security
**Load when:** Working on blockchain security, signature verification, consensus mechanisms
**Version:** 1.0 (Wake 66)

---

## Core Concepts

### 1. Hash Functions

**Purpose:** One-way transformation of data to fixed-size digest

**Properties:**
- **Deterministic:** Same input → same output
- **Pre-image resistance:** Hard to find input from hash
- **Second pre-image resistance:** Hard to find different input with same hash
- **Collision resistance:** Hard to find two inputs with same hash
- **Avalanche effect:** Small input change → large output change

**Common Algorithms:**
- **SHA-256:** Bitcoin, most blockchains (256-bit output)
- **SHA-3 (Keccak):** Ethereum, newer systems (variable output)
- **BLAKE2/BLAKE3:** High-performance alternative
- **RIPEMD-160:** Bitcoin addresses (160-bit output)

**Blockchain Uses:**
- Block linking (chain of hashes)
- Merkle trees (efficient proof of inclusion)
- Address generation (hash of public key)
- Proof-of-work (finding hash with specific properties)
- Content addressing (IPFS, Git)

### 2. Digital Signatures

**Purpose:** Prove authenticity and integrity of messages

**Asymmetric Cryptography:**
- **Private key:** Secret, used to sign
- **Public key:** Shared, used to verify
- **Property:** Can't derive private key from public key

**Common Schemes:**

**ECDSA (Elliptic Curve Digital Signature Algorithm):**
- Bitcoin, Ethereum (secp256k1 curve)
- Smaller keys than RSA (256-bit ≈ 3072-bit RSA)
- Signature: (r, s) pair
- Verification: Check equation using public key

**EdDSA (Edwards-curve Digital Signature Algorithm):**
- Ed25519 (Curve25519)
- Faster, simpler, more secure than ECDSA
- Deterministic signatures (no random nonce)
- Used in: Solana, Polkadot, modern systems

**Schnorr Signatures:**
- Bitcoin Taproot upgrade
- Linear aggregation (multiple signatures → one)
- Simpler security proof than ECDSA

**BLS (Boneh-Lynn-Shacham):**
- Signature aggregation (many → one)
- Used in: Ethereum 2.0, Chia
- Larger keys, slower, but powerful aggregation

**Blockchain Uses:**
- Transaction authorization (prove you own private key)
- Multi-signature wallets (M-of-N signatures required)
- Consensus voting (validators sign blocks)
- Cross-chain bridges (verify messages from other chains)

### 3. Merkle Trees

**Structure:** Binary tree where each node is hash of children

```
        Root Hash
       /          \
   Hash(A,B)    Hash(C,D)
    /    \       /    \
   A      B     C      D
```

**Properties:**
- **Efficient verification:** Prove element in set with O(log n) hashes
- **Tamper-evident:** Changing any leaf changes root
- **Compact proofs:** Don't need entire tree to verify inclusion

**Merkle Proof:**
To prove "B is in tree":
1. Provide: B, A, Hash(C,D)
2. Verify: Hash(Hash(A,B), Hash(C,D)) = Root

**Blockchain Uses:**
- **Bitcoin:** Transactions in block (SPV proofs)
- **Ethereum:** State tree, storage tree, transaction tree
- **Light clients:** Verify without downloading all data
- **Rollups:** Prove state transitions efficiently

**Variants:**
- **Merkle Patricia Trie:** Ethereum state (prefix tree + Merkle)
- **Sparse Merkle Tree:** Efficient for large, sparse datasets
- **Verkle Trees:** Smaller proofs (future Ethereum upgrade)

### 4. Consensus Security

**Byzantine Fault Tolerance (BFT):**
- System works despite malicious actors
- Classic result: Need > 2/3 honest for BFT consensus
- Assumes bounded adversary (can't break crypto)

**Proof-of-Work (PoW):**
- Security from computational cost
- Attack cost: 51% of hash rate
- Properties:
  - Probabilistic finality (deeper = more secure)
  - Permissionless (anyone can mine)
  - Energy intensive

**Proof-of-Stake (PoS):**
- Security from economic stake
- Attack cost: 33% or 51% of stake (depends on protocol)
- Properties:
  - Faster finality
  - Energy efficient
  - "Nothing at stake" problem (solved by slashing)

**Common Attacks:**

**51% Attack:**
- Attacker controls majority of hash rate (PoW) or stake (PoS)
- Can: Reverse transactions, double-spend, censor
- Can't: Steal coins, break signatures, mint coins

**Double-Spend:**
- Send same coins to two recipients
- Requires: Rewriting blockchain history
- Defense: Wait for confirmations (deeper = safer)

**Long-Range Attack (PoS):**
- Attacker rewrites history from genesis
- Defense: Checkpoints, weak subjectivity

**Sybil Attack:**
- Create many fake identities
- Defense: PoW (cost per identity), PoS (stake per identity)

**Eclipse Attack:**
- Isolate node from honest network
- Defense: Diverse peer connections, authenticated peers

### 5. Cryptographic Commitments

**Purpose:** Commit to value without revealing it

**Hash Commitment:**
- Commit: C = Hash(value || nonce)
- Reveal: Show value and nonce, verify hash
- Properties: Hiding (can't see value), binding (can't change value)

**Polynomial Commitment:**
- Commit to polynomial
- Prove evaluations without revealing polynomial
- Used in: ZK-SNARKs, KZG commitments

**Blockchain Uses:**
- **Commit-reveal schemes:** Prevent front-running
- **State commitments:** Rollups commit to state
- **ZK proofs:** Prove statement without revealing data

### 6. Zero-Knowledge Proofs

**Purpose:** Prove statement is true without revealing why

**Properties:**
- **Completeness:** True statement → verifier accepts
- **Soundness:** False statement → verifier rejects (high probability)
- **Zero-knowledge:** Verifier learns nothing except truth of statement

**Types:**

**ZK-SNARKs (Zero-Knowledge Succinct Non-Interactive Arguments of Knowledge):**
- Very small proofs (~200 bytes)
- Fast verification (~milliseconds)
- Requires trusted setup (toxic waste)
- Used in: Zcash, zkSync, StarkWare

**ZK-STARKs (Scalable Transparent Arguments of Knowledge):**
- No trusted setup
- Larger proofs than SNARKs
- Post-quantum secure
- Used in: StarkWare, future systems

**Blockchain Uses:**
- **Privacy:** Prove transaction valid without revealing amount/sender
- **Scalability:** Rollups prove many transactions with one proof
- **Compliance:** Prove age > 18 without revealing exact age

### 7. Threshold Cryptography

**Purpose:** Distribute cryptographic operations across multiple parties

**Threshold Signatures:**
- M-of-N parties must cooperate to sign
- No single party can sign alone
- Used in: Multi-sig wallets, validator committees

**Distributed Key Generation (DKG):**
- Generate key without any party knowing full key
- Each party holds share
- Threshold can reconstruct

**Secret Sharing (Shamir):**
- Split secret into N shares
- Any M shares can reconstruct
- Fewer than M shares reveal nothing

**Blockchain Uses:**
- **Validator committees:** Threshold signatures for consensus
- **Custody:** No single point of failure
- **Randomness:** Distributed random beacons (threshold BLS)

---

## Security Patterns

### Defense in Depth

**Principle:** Multiple layers of security

**Layers:**
1. **Cryptographic:** Strong primitives (SHA-256, Ed25519)
2. **Protocol:** BFT consensus, slashing conditions
3. **Economic:** Attack must be unprofitable
4. **Social:** Governance can respond to attacks
5. **Operational:** Key management, secure infrastructure

### Key Management

**Hot vs Cold:**
- **Hot wallet:** Online, convenient, vulnerable
- **Cold wallet:** Offline, secure, inconvenient
- **Warm wallet:** Threshold between hot and cold

**Best Practices:**
- Never reuse nonces (ECDSA)
- Use deterministic signatures (EdDSA)
- Hardware security modules (HSMs) for high-value keys
- Multi-sig for large amounts
- Regular key rotation for operational keys

### Randomness

**Importance:** Nonces, key generation, consensus leader selection

**Bad Sources:**
- Timestamps (predictable)
- Block hashes (manipulable by miners)
- Pseudo-random without seed

**Good Sources:**
- Hardware RNG
- VRFs (Verifiable Random Functions)
- Threshold randomness (distributed)
- Commit-reveal with multiple parties

---

## Common Vulnerabilities

### Signature Malleability

**Problem:** Attacker modifies valid signature to create different valid signature
**Impact:** Transaction ID changes, breaks dependent transactions
**Solution:** Canonical signatures (BIP 62), signature schemes without malleability

### Weak Randomness

**Problem:** Predictable nonces in ECDSA
**Impact:** Private key recovery from two signatures
**Example:** PlayStation 3 hack (Sony reused nonce)
**Solution:** Deterministic signatures (RFC 6979), proper RNG

### Hash Collisions

**Problem:** Two inputs produce same hash
**Impact:** Fake transactions accepted, Merkle proof forgery
**Solution:** Use collision-resistant hashes (SHA-256, not MD5)

### Timing Attacks

**Problem:** Execution time reveals secret information
**Impact:** Private key recovery through timing analysis
**Solution:** Constant-time implementations

### Quantum Threats

**Vulnerable:**
- ECDSA, RSA (Shor's algorithm breaks discrete log and factoring)
- Current blockchain signatures

**Resistant:**
- Hash functions (Grover's algorithm only 2x speedup)
- Lattice-based crypto
- Hash-based signatures (SPHINCS+)

**Timeline:** 10-30 years until practical quantum computers

---

## Integration with Blockchain Systems

### Transaction Flow

```
1. User creates transaction
2. Sign with private key (ECDSA/EdDSA)
3. Broadcast to network
4. Validators verify signature
5. Include in block
6. Hash block, link to previous
7. Consensus on block validity
```

### State Verification

```
1. Full node: Store entire state
2. Light client: Store only headers
3. Request Merkle proof for specific state
4. Verify proof against header root
5. Trust state without downloading everything
```

### Cross-Chain Security

**Challenge:** Verify events on Chain A from Chain B

**Solutions:**
- **Light clients:** Chain B runs light client of Chain A
- **Relayers:** Submit proofs of Chain A events to Chain B
- **Threshold signatures:** Validator committee signs cross-chain messages
- **ZK proofs:** Prove Chain A state transition on Chain B

---

## Load When

- Implementing signature verification
- Designing consensus mechanisms
- Building cross-chain bridges
- Analyzing security vulnerabilities
- Working on privacy features
- Optimizing cryptographic operations
- Reviewing Tockchain security model
