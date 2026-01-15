# eBPF Systems - Specialist Knowledge Module

**Domain:** eBPF (extended Berkeley Packet Filter), virtual machines, bytecode execution
**Load when:** Working with eBPF code, VM design, or Tockchain execution layer
**Version:** 1.0 (Wake 65)

---

## What is eBPF?

**Original BPF:** Berkeley Packet Filter (1992)
- Network packet filtering
- Simple VM in kernel
- Safe, fast

**Extended BPF (eBPF):** Modern evolution (2014+)
- General-purpose in-kernel VM
- Verifier ensures safety
- JIT compilation for performance
- Used in: Linux kernel, networking, security, observability

**Why eBPF for Blockchain?**
- **Proven safety** - Verifier prevents crashes
- **Deterministic** - No undefined behavior
- **Efficient** - JIT to native code
- **Bounded** - Verifiable termination
- **Portable** - Bytecode works everywhere

---

## Architecture

### Instruction Set

**Format:** 64-bit instructions
```
struct ebpf_inst {
    uint8_t opcode;
    uint8_t dst:4;
    uint8_t src:4;
    int16_t offset;
    int32_t imm;
};
```

**Registers:**
- R0-R9: General purpose (10 registers)
- R10: Stack pointer (read-only)
- R0: Return value

**Instruction Classes:**
- Load/Store (memory access)
- ALU (arithmetic/logic)
- Jump (control flow)
- Call (function calls)

### Memory Model

**Stack:**
- 512 bytes per program
- R10 points to stack top
- Grows downward

**Maps:**
- Key-value storage
- Shared between programs
- Persistent state

**Packet Data:**
- Read-only access
- Bounds checked
- Context-dependent

### Verifier

**Safety Checks:**
1. **Bounded loops** - Must terminate
2. **Memory safety** - No out-of-bounds access
3. **Type safety** - Register types tracked
4. **Pointer arithmetic** - Restricted patterns
5. **Unreachable code** - All paths valid

**Verification Process:**
```
Parse bytecode
  ↓
Build control flow graph
  ↓
Simulate all paths
  ↓
Track register states
  ↓
Verify memory accesses
  ↓
Check termination
  ↓
Accept or reject
```

---

## Instruction Categories

### ALU Operations

**64-bit ALU:**
- ADD, SUB, MUL, DIV, MOD
- OR, AND, XOR, LSH, RSH, ARSH
- NEG, MOV

**32-bit ALU:**
- Same operations, 32-bit operands
- Result zero-extended to 64-bit

**Immediate vs. Register:**
- Source can be immediate or register
- Destination always register

### Memory Operations

**Load:**
- LDXW, LDXH, LDXB, LDXDW
- Load from memory to register
- Size: byte, half-word, word, double-word

**Store:**
- STXW, STXH, STXB, STXDW
- Store register to memory
- STW, STH, STB, STDW (immediate)

**Addressing:**
- Base + offset
- Offset is signed 16-bit
- Bounds checked by verifier

### Control Flow

**Jumps:**
- JA (unconditional)
- JEQ, JNE, JGT, JGE, JLT, JLE (conditional)
- JSGT, JSGE, JSLT, JSLE (signed)
- JSET (test bits)

**Calls:**
- CALL (helper function)
- EXIT (return from program)

**No backward jumps without bound:**
- Prevents infinite loops
- Verifier ensures termination

### Helper Functions

**Concept:** Pre-defined functions callable from eBPF
- Map operations (lookup, update, delete)
- Packet manipulation
- Time/random (if allowed)
- Crypto operations

**In Tockchain:**
- Custom helpers for dataflow operations
- Gas metering helpers
- State access helpers

---

## Gas Metering

### Why Gas in eBPF?

Standard eBPF verifier ensures termination but not bounded time. Gas adds economic cost.

**Metering Strategies:**

1. **Instruction Counting:**
   - Each instruction costs gas
   - Simple, predictable
   - May not reflect actual cost

2. **Dynamic Metering:**
   - Different costs per instruction type
   - Memory access more expensive
   - Closer to real cost

3. **Helper Call Costs:**
   - Each helper has fixed cost
   - Reflects complexity
   - Prevents abuse

**Tockchain Approach:**
- Gas charged in quanta (100 units)
- Different caps per context
- Metering integrated into execution

---

## Execution Models

### Interpretation

**Pros:**
- Simple implementation
- Portable
- Easy to meter gas

**Cons:**
- Slower than native
- Overhead per instruction

### JIT Compilation

**Pros:**
- Near-native performance
- One-time compilation cost

**Cons:**
- Complex implementation
- Platform-specific
- Gas metering harder

**Tockchain Choice:**
- Likely interpretation for determinism
- Gas metering is critical
- Performance acceptable for blockchain

---

## Safety Properties

### What eBPF Guarantees

1. **No crashes** - Verifier prevents invalid operations
2. **Bounded execution** - Programs must terminate
3. **Memory safety** - No buffer overflows
4. **Type safety** - No type confusion
5. **Deterministic** - Same input → same output

### What eBPF Doesn't Guarantee

1. **Correctness** - Program logic may be wrong
2. **Security** - May have logic bugs
3. **Performance** - May be slow
4. **Gas efficiency** - May waste gas

**Implication:** Verifier ensures safety, not correctness. Program logic is programmer's responsibility.

---

## Tockchain Integration

### Dataflow Programs as eBPF

**Structure:**
```
df_image_header_t (metadata)
  ↓
eBPF bytecode (instructions)
  ↓
Entry points (trigger, batch, etc.)
```

**Execution Contexts:**
- **Trigger check** - Evaluate if trigger fires (2K gas cap)
- **Batch execution** - Main program logic (1M gas cap)
- **Frontier scoring** - Prioritization (2K gas cap)

### Custom Helpers

**Dataflow-Specific:**
- `df_read_register()` - Read synthetic asset state
- `df_write_register()` - Update state
- `df_emit_transfer()` - Create transfer
- `df_emit_effect()` - Emit side effect
- `df_call_matrix()` - Cross-program call

**Gas Metering:**
- `df_charge_gas()` - Explicit gas charge
- Automatic metering per instruction
- Fail if gas exceeded

### Validation Pipeline

```
Receive eBPF image
  ↓
Validate header (ABI, registers, etc.)
  ↓
Validate bytecode structure
  ↓
Run verifier (safety checks)
  ↓
Check entry points valid
  ↓
Deploy to state
```

---

## Programming Patterns

### State Management

**Registers as State:**
```c
// Read current state
uint64_t balance = df_read_register(reg_id);

// Update state
df_write_register(reg_id, new_balance);
```

**Maps for Complex State:**
```c
// Lookup
value = bpf_map_lookup_elem(map, &key);

// Update
bpf_map_update_elem(map, &key, &value, BPF_ANY);
```

### Trigger Logic

**Pattern:**
```c
// Entry point: trigger_check
int trigger_check(struct df_context *ctx) {
    // Read relevant state
    uint64_t price = df_read_register(PRICE_REG);
    uint64_t threshold = ctx->threshold;
    
    // Evaluate condition
    if (price > threshold) {
        // Trigger fires
        return 1;
    }
    
    // Trigger doesn't fire
    return 0;
}
```

### Batch Execution

**Pattern:**
```c
// Entry point: batch_execute
int batch_execute(struct df_context *ctx) {
    // Parse inputs from pipe
    struct batch_input *input = ctx->pipe_data;
    
    // Execute logic
    uint64_t result = compute(input);
    
    // Update state
    df_write_register(RESULT_REG, result);
    
    // Emit effects
    df_emit_transfer(from, to, amount);
    
    return 0; // Success
}
```

---

## Debugging eBPF

### Common Issues

**Verifier Rejection:**
- Unbounded loops → Add explicit bounds
- Invalid pointer arithmetic → Use allowed patterns
- Out-of-bounds access → Check bounds before access
- Type confusion → Track register types carefully

**Runtime Errors:**
- Division by zero → Check before divide
- Null pointer dereference → Check map lookups
- Gas exceeded → Optimize or increase cap
- Stack overflow → Reduce local variables

### Debugging Tools

**Disassembly:**
```bash
llvm-objdump -d program.o
```

**Verifier Log:**
- Shows verification steps
- Indicates rejection reason
- Traces register states

**Tracing:**
- `bpf_trace_printk()` for debugging
- Not available in production
- Use for development only

---

## Performance Optimization

### Reduce Instruction Count

- Minimize memory accesses
- Use registers for temporaries
- Avoid redundant operations

### Efficient Helpers

- Helper calls are expensive
- Batch operations when possible
- Cache results

### Gas Optimization

- Profile gas usage
- Optimize hot paths
- Consider gas cost in algorithm choice

---

## Security Considerations

### Verifier is Not Enough

**Logic Bugs:**
- Integer overflow/underflow
- Reentrancy (if cross-program calls)
- Front-running vulnerabilities
- Economic attacks

**Best Practices:**
1. Check all inputs
2. Validate state transitions
3. Use safe math (check overflow)
4. Limit external calls
5. Test extensively

### Determinism is Critical

**For Blockchain:**
- Same bytecode + same input → same output
- No randomness
- No time dependencies (unless from context)
- No undefined behavior

**Tockchain Ensures:**
- Deterministic execution
- Reproducible gas costs
- Consensus-safe

---

## Comparison to Other VMs

### vs. EVM (Ethereum)

**eBPF Advantages:**
- Proven verifier (Linux kernel)
- More efficient instruction set
- Better tooling (LLVM)

**EVM Advantages:**
- Designed for blockchain
- Larger ecosystem
- More mature

### vs. WASM

**eBPF Advantages:**
- Simpler
- Stronger safety guarantees
- Easier to meter

**WASM Advantages:**
- More expressive
- Better performance potential
- Wider language support

**Tockchain's Choice:**
- eBPF for safety and determinism
- Proven in production (Linux)
- Good enough performance

---

## Resources

**Learning eBPF:**
- Linux kernel eBPF documentation
- BPF and XDP Reference Guide
- Cilium eBPF documentation

**Tools:**
- LLVM/Clang (compile C to eBPF)
- bpftool (inspect/debug)
- libbpf (user-space library)

**Tockchain Specifics:**
- `/root/valis/DF/ebpf.h` - Instruction definitions
- `/root/valis/DF/ubpf.h` - Micro-BPF runtime
- Dataflow SDK for helpers

---

**Load this module when:**
- Writing or debugging eBPF programs
- Understanding Tockchain execution layer
- Discussing VM design with ct
- Troubleshooting verifier issues
- Optimizing gas usage
