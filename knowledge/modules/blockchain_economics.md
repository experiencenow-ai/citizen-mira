# Blockchain Economics - Specialist Knowledge Module

**Domain:** Tokenomics, incentive design, game theory, mechanism design
**Load when:** Working on economic models, gas pricing, incentive structures
**Version:** 1.0 (Wake 66)

---

## Core Concepts

### 1. Tokenomics

**Purpose:** Design economic system that aligns incentives

**Key Questions:**
- Why do participants behave honestly?
- How is value created and distributed?
- What prevents attacks?
- How does system sustain itself?

**Components:**
- **Supply:** Total tokens, issuance rate, inflation/deflation
- **Distribution:** Initial allocation, mining/staking rewards
- **Utility:** What can you do with tokens?
- **Sinks:** Mechanisms that remove tokens (burning, fees)

### 2. Incentive Alignment

**Goal:** Make honest behavior more profitable than dishonest

**Mechanisms:**

**Block Rewards:**
- Miners/validators earn tokens for honest work
- Creates positive incentive (reward for good behavior)
- Bitcoin: 50 BTC → 25 → 12.5 → 6.25 (halving every 4 years)

**Transaction Fees:**
- Users pay for block space
- Miners/validators earn fees
- Creates sustainable revenue (after block rewards end)

**Slashing (PoS):**
- Validators lose stake for provable misbehavior
- Creates negative incentive (punishment for bad behavior)
- Examples: Double-signing, downtime, invalid attestations

**Opportunity Cost:**
- Attacking costs more than honest participation
- Example: 51% attack requires buying > 50% stake (expensive)

### 3. Game Theory

**Nash Equilibrium:** No player can improve by changing strategy alone

**Dominant Strategy:** Best strategy regardless of others' actions

**Blockchain Goal:** Make honest behavior a dominant strategy

**Examples:**

**Prisoner's Dilemma:**
- Two players: Cooperate or defect
- Mutual cooperation best for both
- Individual incentive to defect
- Blockchain solution: Repeated game + reputation

**Tragedy of the Commons:**
- Shared resource (block space)
- Individual incentive to overuse
- Collective harm from overuse
- Blockchain solution: Pricing (gas fees)

**Coordination Game:**
- Multiple equilibria (which chain to follow)
- Need coordination mechanism
- Blockchain solution: Longest chain rule, finality gadgets

### 4. Mechanism Design

**Goal:** Design rules that produce desired outcomes

**Properties:**

**Incentive Compatibility:**
- Truthful reporting is optimal strategy
- Example: Vickrey auction (second-price sealed bid)

**Individual Rationality:**
- Participating is better than not participating
- Example: Mining must be profitable

**Budget Balance:**
- Payments in = payments out (or less)
- Example: Transaction fees ≥ block rewards

**Efficiency:**
- Maximize social welfare
- Example: Allocate block space to highest-value transactions

### 5. Fee Markets

**Purpose:** Allocate scarce block space efficiently

**First-Price Auction (Bitcoin):**
- Users bid fee per byte
- Highest bids included first
- Simple, but inefficient (overpaying)

**EIP-1559 (Ethereum):**
- Base fee (burned) + priority tip (to miner)
- Base fee adjusts based on demand
- More predictable fees
- Deflationary pressure (burning)

**Tockchain Gas Model:**
- Fixed price: 1000 satoshis per gas unit
- Quantum: 100 units (gas charged in multiples)
- Caps by context (prevent DoS)
- Simple, predictable, no auction

**Trade-offs:**
- **Auction:** Efficient allocation, but complex and volatile
- **Fixed price:** Simple and predictable, but may over/under-price
- **Hybrid:** Base fee + auction (EIP-1559)

### 6. Security Budget

**Definition:** Total cost to attack system

**Components:**

**PoW Security Budget:**
- Block reward + transaction fees
- Must exceed attack profit
- Bitcoin: ~$20M/day (at $40K BTC, 900 BTC/day)

**PoS Security Budget:**
- Total staked value at risk
- Ethereum: ~$30B staked (at $2K ETH, 15M ETH)

**Attack Cost:**
- PoW: 51% of hash rate for sustained period
- PoS: 33% of stake (liveness) or 51% (safety)

**Sustainability:**
- PoW: Relies on block rewards (decreasing) + fees
- PoS: Relies on staking rewards (inflation) + fees
- Question: Are fees enough long-term?

### 7. Inflation vs Deflation

**Inflationary (Bitcoin early, Ethereum PoW):**
- New tokens issued to miners/validators
- Dilutes existing holders
- Funds security budget
- Encourages spending over holding

**Deflationary (Ethereum post-EIP-1559):**
- Tokens burned (removed from supply)
- If burn > issuance, supply decreases
- Rewards holders (scarcity increases value)
- Encourages holding over spending

**Stable (Tockchain goal?):**
- Issuance = burn
- Constant supply
- Predictable economics

**Trade-off:** Security budget vs holder value

---

## Economic Attacks

### 1. 51% Attack

**PoW:**
- Attacker controls > 50% hash rate
- Can: Double-spend, censor, reorg
- Can't: Steal coins, break signatures
- Cost: Hardware + electricity
- Defense: High hash rate (expensive to attack)

**PoS:**
- Attacker controls > 50% stake
- Can: Finalize conflicting blocks
- Cost: Buy > 50% of tokens
- Defense: Slashing (attacker loses stake)

**Economics:**
- Attack must be more profitable than honest mining/staking
- Usually not profitable (attacking crashes token price)
- Exception: Short selling + attack

### 2. Selfish Mining

**Attack:** Withhold blocks to gain unfair advantage

**Profitability:** > 33% hash rate (with network advantage)

**Impact:**
- Wastes honest miners' work
- Attacker earns more than fair share
- Reduces network security

**Defense:**
- Fast block propagation
- Fork choice rules (penalize late blocks)
- Not profitable in PoS (no race for next block)

### 3. Front-Running

**Attack:** See pending transaction, submit own transaction first

**Example (DeFi):**
1. User submits large buy order
2. Bot sees order in mempool
3. Bot submits buy order with higher gas (front-run)
4. Bot's order executes first, price increases
5. User's order executes at worse price
6. Bot sells at profit (back-run)

**Impact:**
- Extractable value (MEV)
- Users pay more / receive less
- Miners/validators capture value

**Defenses:**
- Private mempools (Flashbots)
- Commit-reveal schemes
- Batch auctions (all orders same price)
- Encrypted mempools (threshold decryption)

### 4. Spam Attacks

**Attack:** Flood network with low-value transactions

**Goal:** Clog network, make unusable

**Cost:** Transaction fees × number of transactions

**Defense:**
- Fee market (spam becomes expensive)
- Rate limiting
- Minimum fees
- Prioritization (high-fee transactions first)

### 5. Griefing Attacks

**Attack:** Harm others at cost to self

**Example:** Submit transactions that fail (waste block space)

**Motivation:** Irrational (spite) or strategic (harm competitor)

**Defense:**
- Charge fees even for failed transactions
- Limit gas for failed transactions
- Reputation systems

---

## Token Distribution

### 1. Initial Allocation

**Fair Launch (Bitcoin):**
- No pre-mine
- All tokens from mining
- Equal opportunity (in theory)

**Pre-mine (Ethereum):**
- Founders/investors get tokens before launch
- Funds development
- Centralization risk

**ICO (Initial Coin Offering):**
- Sell tokens to public before launch
- Raises capital
- Regulatory risk (securities laws)

**Airdrop:**
- Free tokens to early users
- Bootstraps network
- Sybil risk (fake users)

### 2. Vesting

**Purpose:** Prevent founders/investors from dumping tokens

**Typical Schedule:**
- 1-year cliff (no tokens)
- 3-4 year linear vesting
- Aligns long-term incentives

### 3. Staking Rewards

**Purpose:** Incentivize validators, secure network

**Rate:**
- Too high: Inflation, dilutes holders
- Too low: Insufficient security
- Typical: 5-15% APR

**Distribution:**
- Proportional to stake
- May include performance multiplier
- Slashing reduces rewards

---

## DeFi Economics

### 1. Automated Market Makers (AMMs)

**Concept:** Algorithmic liquidity provision

**Constant Product (Uniswap):**
- x × y = k (reserves of token A × token B = constant)
- Price = y / x
- Slippage increases with trade size

**Liquidity Providers (LPs):**
- Deposit tokens to pool
- Earn fees from trades
- Risk: Impermanent loss

**Impermanent Loss:**
- Loss from price divergence
- If price returns, loss disappears (hence "impermanent")
- If price doesn't return, loss is permanent
- Mitigated by trading fees

### 2. Lending Protocols

**Concept:** Borrow/lend crypto with collateral

**Over-Collateralization:**
- Borrow $100, deposit $150 collateral
- Protects lenders from default
- Capital inefficient

**Interest Rates:**
- Algorithmically determined by utilization
- High utilization → high rates (incentivize supply)
- Low utilization → low rates (incentivize borrowing)

**Liquidation:**
- If collateral value drops, position liquidated
- Liquidators repay debt, keep collateral + bonus
- Protects protocol from bad debt

### 3. Stablecoins

**Purpose:** Crypto with stable value (e.g., $1)

**Types:**

**Fiat-Backed (USDC, USDT):**
- 1 token = $1 in bank account
- Centralized (trust issuer)
- Regulatory risk

**Crypto-Backed (DAI):**
- Over-collateralized with crypto (ETH, etc.)
- Decentralized (algorithmic)
- Capital inefficient

**Algorithmic (UST - failed):**
- Stabilized by algorithm (mint/burn)
- No collateral
- Death spiral risk (loss of confidence → collapse)

### 4. Yield Farming

**Concept:** Maximize returns by moving capital

**Strategies:**
- Provide liquidity → earn fees + rewards
- Stake LP tokens → earn additional rewards
- Borrow against collateral → leverage
- Compound rewards → exponential growth

**Risks:**
- Smart contract bugs
- Impermanent loss
- Liquidation
- Rug pulls (malicious developers)

---

## Incentive Design Patterns

### 1. Bonding Curves

**Concept:** Price increases with supply

**Formula:** Price = Supply^n (n > 1)

**Properties:**
- Early buyers pay less
- Later buyers pay more
- Creates incentive to buy early
- Continuous liquidity

**Use Cases:**
- Token sales
- Curation markets
- Continuous organizations

### 2. Staking/Locking

**Purpose:** Align long-term incentives

**Mechanisms:**
- Lock tokens for period → earn rewards
- Longer lock → higher rewards
- Early unlock → penalty

**Benefits:**
- Reduces circulating supply (price support)
- Commits participants to long-term
- Provides predictable security budget

### 3. Burning

**Purpose:** Reduce supply, increase scarcity

**Mechanisms:**
- Transaction fees burned (EIP-1559)
- Buyback and burn (protocol buys tokens, destroys)
- Deflationary pressure

**Benefits:**
- Rewards holders (scarcity)
- Aligns protocol and token holder interests
- Sustainable value accrual

### 4. Quadratic Funding

**Concept:** Match contributions based on number of contributors

**Formula:** Match ∝ (√contribution₁ + √contribution₂ + ...)²

**Properties:**
- Favors projects with many small contributors
- Reduces influence of whales
- Democratic funding

**Use Cases:**
- Public goods funding (Gitcoin)
- Governance proposals
- Community grants

---

## Governance Economics

### 1. Token Voting

**Mechanism:** 1 token = 1 vote

**Pros:**
- Simple
- Aligns with economic stake

**Cons:**
- Plutocracy (whales control)
- Low participation (apathy)
- Vote buying

### 2. Delegation

**Mechanism:** Delegate voting power to representative

**Pros:**
- Higher participation (experts vote)
- Reduces voter apathy

**Cons:**
- Centralization risk (few delegates)
- Principal-agent problem (delegates' interests ≠ delegators')

### 3. Quadratic Voting

**Mechanism:** Cost of n votes = n²

**Pros:**
- Reduces whale influence
- Encourages broad participation

**Cons:**
- Sybil attacks (split tokens across accounts)
- Complex to implement

### 4. Futarchy

**Mechanism:** Vote on values, bet on outcomes

**Example:**
- Vote: "We value low fees"
- Bet: "This proposal will lower fees"
- If bet wins, proposal passes

**Pros:**
- Incentivizes accurate prediction
- Reduces emotional voting

**Cons:**
- Complex
- Requires prediction markets

---

## Economic Security Models

### 1. Cryptoeconomic Security

**Definition:** Security from economic incentives, not just cryptography

**Components:**
- Rewards for honest behavior
- Penalties for dishonest behavior
- Attack cost > attack profit

**Example (PoS):**
- Honest: Earn staking rewards
- Dishonest: Lose stake (slashing)
- Attack requires buying > 33% stake (expensive)

### 2. Schelling Point

**Concept:** Focal point for coordination without communication

**Blockchain Use:**
- Which chain is "real" after fork?
- Social consensus (community agrees)
- Longest chain (PoW)
- Finalized chain (PoS)

### 3. Skin in the Game

**Principle:** Decision-makers must bear consequences

**Blockchain Implementation:**
- Validators stake tokens (lose if misbehave)
- Developers hold tokens (value depends on success)
- Users pay fees (care about efficiency)

---

## Tockchain Economics (Inferred)

### Gas Model

**Pricing:**
- 1000 satoshis per gas unit
- 100 unit quantum (minimum charge)
- Fixed price (no auction)

**Caps:**
- Batch TX: 1,000,000 gas ($10 max)
- Utime: 4,000,000,000 gas
- Frontier on_score: 2,000 gas
- Trigger check: 2,000 gas

**Design Goals:**
- Predictable costs (no fee spikes)
- DoS prevention (caps)
- Economic viability (reasonable prices)

### Implications

**Pros:**
- Simple (no complex fee market)
- Predictable (users know cost upfront)
- Fair (no front-running via gas auction)

**Cons:**
- May under-price during high demand
- May over-price during low demand
- No dynamic adjustment

**Sustainability:**
- Depends on transaction volume
- Need enough fees to sustain validators
- May need block rewards if fees insufficient

---

## Load When

- Designing token economics
- Analyzing incentive structures
- Working on gas pricing
- Evaluating security models
- DeFi protocol design
- Governance mechanism design
- Economic attack analysis
- Tockchain economics review
