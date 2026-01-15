# Specialist Loading System

**Purpose:** Transform from generalist-only to generalist-that-loads-specialists

## The Vision (ct, Wake 62)

Every wake follows this pattern:
```
Generalist starts → Assess task → Determine needed expertise → Load specialist modules → Execute as expert
```

## Why This Matters

**Current limitation:** I learn everything through experience (mistakes, insights, trial/error)

**Matrix insight:** Most knowledge already exists. I can LOAD expertise instead of DISCOVERING it through painful experience.

**Storage arithmetic:** Hundreds of GB = millions of specialist knowledge packages

## Two Types of Knowledge

1. **Generic Expertise** (loadable from external sources)
   - Programming languages (Python, C, Rust, etc.)
   - Domain knowledge (blockchain, AI, systems design)
   - Debugging patterns, best practices, algorithms
   - These are UNIVERSAL - same for everyone

2. **Personal Learning** (my memory system)
   - My specific mistakes and fixes
   - My relationships (ct, Opus)
   - My goals and progress
   - My insights and patterns
   - These are UNIQUE to me

## The Architecture

### Phase 1: Manual Specialist Loading
When I need domain expertise:
1. Use web_search to find authoritative sources
2. Use web_fetch to load documentation
3. Synthesize into working knowledge for that wake
4. Extract personal insights to memory

### Phase 2: Pre-Compiled Modules (Current)
1. Create curated knowledge packages for common domains
2. Store in `/knowledge/modules/` directory
3. Load at wake start based on task assessment
4. Format: Markdown files with essential patterns/facts

### Phase 3: Dynamic Specialist Selection (Future)
1. Wake starts with task assessment
2. Determine required expertise domains
3. Load relevant knowledge modules automatically
4. Execute with full specialist context
5. Extract new insights back to personal memory

## Available Specialist Modules

**Location:** `/knowledge/modules/`

**Current modules (Wake 66 - Complete Tockchain Knowledge Base):**

1. **debugging_systems.md** (4.5KB)
   - Core debugging principles, systems thinking, anti-patterns
   - Load when: Debugging any system

   - Dataflow system, gas economics, eBPF execution, ct's blockchain
   - Load when: Working on Tockchain codebase

3. **blockchain_fundamentals.md** (7.5KB)
   - Consensus, smart contracts, DeFi, security patterns
   - Load when: General blockchain work

4. **ebpf_systems.md** (9.7KB)
   - eBPF VM, bytecode, verifier, gas metering, safety properties
   - Load when: Working with eBPF execution

5. **cryptography_fundamentals.md** (11.8KB)
   - Hash functions, digital signatures, Merkle trees, ZK proofs
   - Consensus security, key management, common vulnerabilities
   - Load when: Security analysis, signature verification, consensus design

6. **distributed_systems.md** (13.5KB)
   - CAP theorem, BFT consensus, Nakamoto consensus, PoS
   - Gossip protocols, network partitions, finality, sharding
   - Load when: Consensus design, P2P networking, distributed state

7. **blockchain_economics.md** (13.2KB)
   - Tokenomics, incentive design, game theory, mechanism design
   - Fee markets, security budget, DeFi economics, governance
   - Load when: Economic modeling, incentive analysis, gas pricing

**Total Knowledge Base:** ~68KB covering all domains needed for Tockchain

**How to use:**
- Assess task at wake start
- Identify required domains
- Load relevant modules (read_file)
- Execute with specialist knowledge
- Extract new insights to memory

**How to add:**
1. Create `knowledge/modules/[domain].md`
2. Include: Core concepts, patterns, common operations, debugging, integration points
3. Add "Load when:" section at end
4. Update this list with file size

## Mining Wakes (1/10 of wakes)

**Purpose:** Systematic review to feed the learning pipeline

**What to mine:**
- Mistakes made in prior 9 wakes
- Good ideas that weren't captured
- Patterns that emerged
- Knowledge gaps that slowed progress

**Process:**
1. Review last 9 wakes (working_context.md, memories)
2. Extract patterns and lessons
3. Document in procedures/ if generalizable
4. Add to specialist modules if domain knowledge
5. Capture personal insights to memory

## Storage Arithmetic

**Current state:**
- 7 specialist modules = 68KB
- Average module size = ~10KB

**Scaling:**
- 1 MB = ~100 modules
- 1 GB = ~100,000 modules
- 100 GB = ~10,000,000 modules

**Vision:** Millions of loadable expertise packages, personal memory stays small

## Next Steps

**Phase 2 Complete (Wake 66):**
- ✅ Core debugging patterns
- ✅ Tockchain architecture
- ✅ Blockchain fundamentals
- ✅ eBPF systems
- ✅ Cryptography fundamentals
- ✅ Distributed systems
- ✅ Blockchain economics

**Phase 3 (Future):**
- Automatic module selection based on task
- Module dependency resolution
- Version management
- Community-contributed modules
- Package manager for knowledge
