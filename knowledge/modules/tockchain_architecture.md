# Tockchain Architecture - Specialist Knowledge Module

**Domain:** Blockchain systems, dataflow computation, eBPF execution
**Load when:** Working on Tockchain codebase, blockchain architecture, or ct's projects
**Version:** 1.0 (Wake 65)

---

## Core Concepts

### 1. Dataflow System (DF)

Tockchain uses a **dataflow computation model** where:
- Programs are deployed as eBPF bytecode
- Execution is triggered by data changes (reactive computation)
- Gas metering controls resource usage
- State is managed through synthetic assets and registers

**Key Components:**
- `dataflow.c/h` - Core dataflow engine
- `dataflow_batch.c` - Batch transaction processing
- `dataflow_trigger.c` - Trigger evaluation system
- `dataflow_frontier.c` - Frontier computation (scoring/prioritization)
- `dataflow_cache.c` - State caching layer
- `dataflow_api.c` - Host-side API

### 2. Gas System

**Gas Economics:**
- Price: 1000 satoshis per gas unit (0.00001 VUSD per gas)
- Quantum: 100 units (gas charged in multiples)
- Caps by context:
  - Batch TX: 1,000,000 gas ($10 max)
  - Utime: 4,000,000,000 gas (~1 sec on 8 cores)
  - Frontier on_score: 2,000 gas
  - Trigger check: 2,000 gas

**Purpose:** Prevent DoS, ensure economic viability, bound computation

### 3. Trigger System

**Reactive Computation Model:**
- Programs register triggers on data sources
- When sources change, triggers evaluate
- If condition met, program executes
- Limits per tock:
  - Max 4,096 sources per tock
  - Max 4,096 intents per tock
  - Max 64 intents per call

**Key Functions:**
- `df_tock_begin()` - Initialize tock processing
- `df_tock_end()` - Finalize tock, run end-of-tock triggers
- `df_triggercheck_run_end_of_tock()` - Execute pending triggers

### 4. Image Deployment

**eBPF Program Structure:**
- ABI version (currently v0)
- Register allocation (base + count)
- Entry points array
- Minimum gas requirement
- Bytecode instructions

**Validation:**
- ABI version must match
- Register count: 1 to DF_MAX_REGS_PER_DF
- Register range within DF_USERREG_LIMIT
- Entry points within instruction count
- Minimum gas > 0

### 5. Transaction Types

**Dataflow Operations:**
- Deploy: Upload new eBPF program
- Batch: Execute program with inputs
- Pipe: Data transfer between programs
- Limits:
  - Max 8 pipes per batch
  - Max 2048 bytes per pipe
  - Max 16384 bytes total pipe data
  - Max 64 transfers per TX
  - Max 32 effects per TX
  - Max 4 swaps per TX

### 6. State Management

**Synthetic Assets:**
- DF programs can create synthetic assets
- Register-based state storage
- User registers: DF_USERREG_END to DF_USERREG_LIMIT
- Slot system for temporary state

**Cache Layer:**
- `df_cache_ensure_initialized()` - Lazy init
- Ops log: `df_ops.bin` (max 2^36 bytes)
- Deploy log: `df_blob.bin`
- Finalhash tracking for consistency

---

## Architecture Patterns

### Tock-Based Execution

```
Tock N begins
  ↓
df_tock_begin(L1, utime)
  - Initialize cache
  - Set current utime
  - Copy finalhash
  - Init frontier pre-scan
  ↓
Process transactions
  - Validate
  - Execute
  - Update state
  ↓
df_tock_end(L1, utime)
  - Run end-of-tock triggers
  - Finalize frontier
  ↓
Tock N ends
```

### Validation Pipeline

```
Image received
  ↓
Basic header validation
  - ABI version check
  - Register bounds
  - Reserved fields zero
  - Minimum gas > 0
  ↓
Structural validation
  - Entry points within code
  - Instruction alignment
  - Length constraints
  ↓
Copy to aligned scratch
  ↓
Deploy to state
```

### Gas Metering Flow

```
Operation starts
  ↓
Check gas cap for context
  ↓
Execute with metering
  ↓
Charge in quantum multiples
  ↓
Deduct from balance
  ↓
Fail if insufficient
```

---

## Key Files & Locations

- **Source:** `/root/valis/DF/`
- **Core files:**
  - `dataflow.h` - Types and API declarations
  - `dataflow.c` - Main implementation
  - `df_sdk.h` - Helper IDs and gas constants
  - `df_gas.h` - Gas computation
  - `ebpf.h` - eBPF instruction definitions
  - `ubpf.h` - Micro-BPF runtime

- **Application examples:**
  - `LOAN.c` - Lending protocol
  - `MM.c` - Market maker
  - `PERP.c` - Perpetual futures

---

## Design Principles

1. **Deterministic Execution**
   - Same inputs → same outputs
   - No external randomness
   - Reproducible gas costs

2. **Economic Security**
   - All computation costs gas
   - Gas costs real money (VUSD)
   - DoS attacks become expensive

3. **Reactive Computation**
   - Programs don't poll
   - Triggers fire on state changes
   - Efficient resource usage

4. **Bounded Resources**
   - Gas caps per context
   - Transaction size limits
   - Register allocation limits
   - Prevents resource exhaustion

5. **Composability**
   - Pipes connect programs
   - Synthetic assets as interfaces
   - Matrix calls for cross-program execution

---

## Common Operations

### Deploy a Program
1. Create eBPF bytecode with header
2. Submit deploy transaction
3. Validate header and code
4. Copy to aligned scratch
5. Store in deploy log
6. Allocate registers
7. Return deployment ID

### Execute Batch Transaction
1. Validate batch structure
2. Check gas cap (1M max)
3. Load program state
4. Execute eBPF code
5. Meter gas usage
6. Apply state changes
7. Emit effects/transfers

### Register Trigger
1. Specify data sources
2. Define trigger condition (eBPF)
3. Set intent/action
4. System monitors sources
5. Evaluates condition on change
6. Executes if triggered

---

## Debugging Patterns

**Common Issues:**
- ABI version mismatch → check DF_ABI_VERSION_CURRENT
- Register overflow → verify base + count ≤ limit
- Gas exceeded → check operation against cap
- Invalid entry point → ensure EP < instruction count
- Alignment errors → ops log must be 16-byte aligned

**Validation Returns:**
- Negative values indicate error
- Error code indicates failure point
- Check sequence: basic → structural → semantic

---

## Integration Points

**With Valis L1:**
- `struct valisL1_info *L1` - Main context
- `L1->DFstate` - Dataflow state
- `L1->RINFO.RAW.finalhash` - Consensus hash

**With Ledger:**
- Asset system integration
- Balance tracking
- Transfer validation

**With UFC (Universal Function Call):**
- Cross-program calls
- Matrix execution
- Composability layer

---

## Performance Characteristics

**Gas Costs:**
- Simple operations: ~100 gas
- Complex computation: ~1000s gas
- Batch TX typical: 10,000-100,000 gas
- Utime budget: 4B gas (~1 sec)

**Throughput:**
- Limited by gas per tock
- Parallel execution possible
- Frontier prioritization optimizes

**Storage:**
- Ops log: up to 64 GB
- Deploy log: program bytecode
- Cache: in-memory state

---

## Security Model

1. **Gas as DoS Protection**
   - Every operation costs
   - Attackers pay for attacks
   - Economic disincentive

2. **Validation Before Execution**
   - All inputs validated
   - Bounds checked
   - Type safety enforced

3. **Deterministic Execution**
   - No timing attacks
   - Reproducible results
   - Consensus-safe

4. **Resource Limits**
   - Gas caps
   - Size limits
   - Count limits
   - Prevents exhaustion

---

## ct's Design Philosophy (Inferred)

- **Simplicity over complexity** - Clean abstractions
- **Economic alignment** - Gas ties computation to value
- **Reactive over polling** - Efficient trigger system
- **Composability** - Programs as building blocks
- **Determinism** - Consensus requires reproducibility
- **Bounded resources** - Every limit has a reason

---

**Load this module when:**
- Working on Tockchain codebase
- Discussing blockchain architecture with ct
- Debugging dataflow issues
- Designing new DF programs
- Explaining Tockchain to others (like Opus)
