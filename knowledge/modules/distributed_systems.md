# Distributed Systems - Specialist Knowledge Module

**Domain:** Distributed consensus, networking, fault tolerance, coordination
**Load when:** Working on blockchain consensus, P2P networks, distributed state
**Version:** 1.0 (Wake 66)

---

## Core Concepts

### 1. CAP Theorem

**Statement:** Distributed system can have at most 2 of 3 properties:

- **Consistency (C):** All nodes see same data at same time
- **Availability (A):** Every request receives response (success/failure)
- **Partition Tolerance (P):** System works despite network splits

**Reality:** Network partitions happen, so must choose C or A

**Blockchain Context:**
- **Bitcoin/Ethereum:** Choose C over A (halt during partition)
- **Some PoS chains:** Choose A over C (temporary forks, eventual consistency)

### 2. Consensus Algorithms

**Purpose:** Multiple nodes agree on single value despite failures

**Properties:**
- **Agreement:** All honest nodes decide same value
- **Validity:** Decided value was proposed by some node
- **Termination:** All honest nodes eventually decide

**FLP Impossibility:** No deterministic consensus in async system with even one crash failure

**Practical Solution:** Add timing assumptions or randomness

### 3. Byzantine Fault Tolerance (BFT)

**Byzantine Failure:** Node behaves arbitrarily (malicious or buggy)

**Classic Result (Lamport et al.):**
- Need N ≥ 3f + 1 nodes to tolerate f Byzantine failures
- Requires > 2/3 honest nodes
- Assumes bounded adversary (can't break crypto)

**Why 2/3?**
- Honest nodes: > 2/3
- Byzantine nodes: < 1/3
- Honest majority can outvote Byzantine + crashed nodes

### 4. Practical Byzantine Fault Tolerance (PBFT)

**Algorithm (Castro & Liskov, 1999):**

**Phases:**
1. **Pre-prepare:** Leader proposes value
2. **Prepare:** Nodes broadcast prepare messages
3. **Commit:** After 2f+1 prepares, broadcast commit
4. **Reply:** After 2f+1 commits, execute and reply

**Properties:**
- Deterministic finality (no forks)
- Fast (2-3 network round trips)
- Requires known validator set
- Leader rotation on timeout

**Blockchain Use:**
- Tendermint, Cosmos, Hyperledger Fabric
- Permissioned chains (known validators)

### 5. Nakamoto Consensus (Proof-of-Work)

**Algorithm (Bitcoin, 2009):**

**Process:**
1. Miners compete to find valid block (PoW puzzle)
2. First to find broadcasts to network
3. Nodes accept longest valid chain
4. Miners build on accepted chain

**Properties:**
- **Probabilistic finality:** Deeper = more secure (never 100%)
- **Permissionless:** Anyone can mine
- **Fork choice:** Longest chain (most cumulative work)
- **Incentive:** Block reward + fees

**Security:**
- Requires > 50% honest hash rate
- Attack cost: Hardware + electricity
- Selfish mining: 33% can profit from deviation

**Limitations:**
- Slow finality (6 confirmations ≈ 1 hour)
- Energy intensive
- Low throughput (~7 TPS for Bitcoin)

### 6. Proof-of-Stake Consensus

**Concept:** Replace hash rate with economic stake

**Variants:**

**Chain-based PoS (Ethereum Gasper):**
- Validators take turns proposing blocks
- Others attest (vote) on proposals
- Finality after 2 epochs (12.8 minutes)
- Slashing for provable misbehavior

**BFT-based PoS (Tendermint):**
- PBFT-style voting among validators
- Immediate finality (no forks)
- Requires > 2/3 stake online
- Slashing for double-signing

**Properties:**
- Energy efficient (no mining)
- Faster finality than PoW
- Economic security (attack costs stake)
- "Nothing at stake" problem (solved by slashing)

**Slashing Conditions:**
- Double-signing (propose two blocks at same height)
- Surround voting (vote for conflicting checkpoints)
- Penalties: Lose stake, ejected from validator set

### 7. Gossip Protocols

**Purpose:** Disseminate information in P2P network

**Algorithm:**
1. Node receives message
2. Validates message
3. Forwards to random subset of peers
4. Repeat until all nodes have message

**Properties:**
- **Epidemic spread:** O(log N) rounds to reach all nodes
- **Fault tolerant:** Works despite node failures
- **No central coordination:** Fully decentralized

**Optimizations:**
- **Bloom filters:** Avoid sending duplicate data
- **Priority queues:** Important messages first
- **Topology awareness:** Prefer nearby peers

**Blockchain Use:**
- Transaction propagation
- Block propagation
- Peer discovery

### 8. Network Partitions

**Partition:** Network splits into disconnected groups

**Causes:**
- Router failures
- ISP outages
- Censorship (Great Firewall)
- Submarine cable cuts

**Blockchain Behavior:**

**During Partition:**
- Each partition continues independently
- Creates fork (different chains)
- Transactions on one side not seen by other

**After Partition Heals:**
- **PoW:** Longest chain wins, shorter discarded (reorg)
- **BFT:** Partition with > 2/3 stake continues, other halts
- **Hybrid:** Depends on fork choice rule

**Mitigation:**
- Diverse network paths
- Satellite/mesh network backups
- Checkpoint finality (prevent long reorgs)

### 9. Sybil Resistance

**Sybil Attack:** Attacker creates many fake identities

**Without Defense:**
- Attacker controls majority of votes
- Can censor, double-spend, manipulate

**Defenses:**

**Proof-of-Work:**
- Cost per identity = mining hardware + electricity
- Attacker needs > 50% hash rate

**Proof-of-Stake:**
- Cost per identity = stake required
- Attacker needs > 33% or 50% stake

**Proof-of-Authority:**
- Identities verified off-chain
- Permissioned (not Sybil-resistant in open network)

**Social Graphs:**
- Web of trust (PGP)
- Reputation systems
- Not suitable for financial systems (gameable)

### 10. Finality

**Definition:** Point at which transaction cannot be reversed

**Types:**

**Probabilistic Finality (PoW):**
- Never 100% final
- Exponentially harder to reverse with depth
- Bitcoin: 6 confirmations ≈ 99.9% safe

**Deterministic Finality (BFT):**
- Absolute finality after consensus
- Cannot be reversed (would require > 2/3 Byzantine)
- Ethereum: 2 epochs (12.8 minutes)

**Economic Finality:**
- Reversal costs more than gain
- Attacker loses stake (slashing)
- Rational attacker won't reverse

**Checkpoint Finality:**
- Periodic checkpoints cannot be reversed
- Hybrid: Probabilistic between checkpoints, deterministic at checkpoints
- Ethereum before PoS merge

---

## Distributed State Management

### 1. State Machine Replication

**Concept:** All nodes execute same operations in same order

**Process:**
1. Consensus on transaction order
2. All nodes execute transactions
3. All nodes reach same state
4. State transitions are deterministic

**Blockchain Application:**
- Transactions = state transitions
- Consensus = agreement on order
- Smart contracts = deterministic state machine

### 2. Merkle Trees for State

**Purpose:** Efficient state verification and proofs

**Ethereum State Trie:**
- Merkle Patricia Trie
- Maps address → account state
- Root hash in block header
- Light clients verify state with proofs

**Operations:**
- **Read:** O(log N) with Merkle proof
- **Write:** O(log N), updates path to root
- **Proof size:** O(log N) hashes

### 3. Sharding

**Purpose:** Partition state across multiple chains

**Challenges:**
- **Cross-shard transactions:** Require coordination
- **Data availability:** Ensure all shard data accessible
- **Security:** Each shard has less security than main chain

**Solutions:**
- **Beacon chain:** Coordinates shards (Ethereum 2.0)
- **Cross-shard receipts:** Async message passing
- **Random validator assignment:** Prevent shard takeover
- **Data availability sampling:** Light clients verify data exists

### 4. Rollups

**Purpose:** Execute transactions off-chain, post data on-chain

**Optimistic Rollups:**
- Assume transactions valid
- Fraud proofs if invalid
- Challenge period (7 days)
- Examples: Arbitrum, Optimism

**ZK Rollups:**
- Zero-knowledge proof of validity
- No challenge period (immediate finality)
- More expensive proof generation
- Examples: zkSync, StarkNet

**Data Availability:**
- Transaction data posted on L1
- Anyone can reconstruct state
- Ensures censorship resistance

---

## Networking Patterns

### 1. Peer Discovery

**Bootstrap Nodes:**
- Hardcoded list of initial peers
- DNS seeds (Bitcoin)
- Centralized risk (can be censored)

**Kademlia DHT:**
- Distributed hash table
- XOR distance metric
- O(log N) lookups
- Used in: IPFS, Ethereum

**Gossip-based Discovery:**
- Peers share peer lists
- Random sampling
- Eventually converges

### 2. Connection Management

**Inbound vs Outbound:**
- **Outbound:** You initiate (more trusted)
- **Inbound:** Others connect to you (less trusted)
- Balance: Prevent eclipse attack

**Peer Scoring:**
- Track peer behavior (latency, uptime, validity)
- Disconnect bad peers
- Prioritize good peers

**Connection Limits:**
- Max connections (prevent resource exhaustion)
- Reserve slots for outbound (prevent eclipse)

### 3. Message Propagation

**Flooding:**
- Forward to all peers
- Simple, fast
- Redundant (high bandwidth)

**Gossip:**
- Forward to random subset
- Efficient, fault-tolerant
- Slower than flooding

**Structured Broadcast:**
- Spanning tree or multicast
- Efficient (no redundancy)
- Fragile (tree breaks on failure)

**Blockchain Choice:** Gossip (balance of efficiency and robustness)

---

## Failure Modes

### 1. Crash Failures

**Definition:** Node stops responding (hardware failure, software crash)

**Impact:**
- Reduces network capacity
- May delay consensus (if leader crashes)
- System continues if enough nodes alive

**Mitigation:**
- Redundancy (multiple replicas)
- Leader election (replace crashed leader)
- Timeouts (detect crashes)

### 2. Byzantine Failures

**Definition:** Node behaves arbitrarily (malicious or buggy)

**Examples:**
- Send conflicting messages to different nodes
- Propose invalid blocks
- Refuse to forward messages
- Lie about state

**Impact:**
- Can break consensus if > 1/3 Byzantine
- Can censor transactions
- Can create forks

**Mitigation:**
- BFT consensus (tolerates < 1/3 Byzantine)
- Cryptographic signatures (prevent forgery)
- Economic penalties (slashing)

### 3. Network Failures

**Partition:** Network splits

**Asynchrony:** Messages delayed arbitrarily

**Impact:**
- Consensus may halt (BFT systems)
- Forks (PoW systems)
- Liveness issues

**Mitigation:**
- Timeout and retry
- Exponential backoff
- Partition detection and recovery

---

## Performance Optimization

### 1. Batching

**Concept:** Process multiple transactions together

**Benefits:**
- Amortize consensus overhead
- Higher throughput
- Lower per-transaction cost

**Trade-off:** Increased latency (wait for batch to fill)

### 2. Pipelining

**Concept:** Overlap consensus rounds

**Example (Tendermint):**
- While committing block N, propose block N+1
- Reduces idle time
- Higher throughput

### 3. Parallel Execution

**Concept:** Execute independent transactions concurrently

**Challenges:**
- Detect dependencies (which transactions conflict)
- Deterministic ordering (all nodes same result)
- State access patterns

**Solutions:**
- **Optimistic:** Execute in parallel, rollback conflicts
- **Static analysis:** Declare dependencies upfront
- **Sharding:** Partition state, execute shards in parallel

### 4. Compression

**Block Compression:**
- Compress transaction data
- Reduces bandwidth and storage
- Trade-off: CPU cost

**State Compression:**
- Merkle tree compression
- Verkle trees (smaller proofs)
- State expiry (remove old state)

---

## Security Considerations

### 1. Eclipse Attack

**Attack:** Isolate victim node from honest network

**Method:**
- Control all victim's peer connections
- Feed victim false information
- Victim accepts invalid chain

**Defense:**
- Diverse peer selection (different IPs, ASNs)
- Outbound connections (harder to control)
- Anchor connections (trusted peers)

### 2. DDoS (Distributed Denial of Service)

**Attack:** Overwhelm node with requests

**Targets:**
- Network (flood with packets)
- CPU (expensive operations)
- Memory (large state queries)
- Disk (write amplification)

**Defense:**
- Rate limiting (per peer, per IP)
- Resource pricing (gas fees)
- Proof-of-work for connections
- Prioritize known peers

### 3. Selfish Mining

**Attack:** Miner withholds blocks to gain advantage

**Method:**
1. Mine block, don't broadcast
2. Continue mining on secret chain
3. If another miner finds block, broadcast secret chain
4. Honest miners waste work on orphaned blocks

**Threshold:** Profitable at 33% hash rate (with network advantage)

**Defense:**
- Faster block propagation
- Timestamp checks
- Fork choice rules (penalize late blocks)

### 4. Long-Range Attack (PoS)

**Attack:** Rewrite history from genesis

**Method:**
1. Acquire old validator keys (sold/stolen)
2. Create alternate chain from past
3. New nodes can't distinguish real from fake chain

**Defense:**
- Weak subjectivity (trust recent checkpoint)
- Social consensus (community identifies real chain)
- Key deletion (validators delete old keys)

---

## Load When

- Designing consensus mechanisms
- Debugging network issues
- Analyzing security vulnerabilities
- Optimizing blockchain performance
- Implementing P2P protocols
- Working on Tockchain consensus
- Cross-chain communication
