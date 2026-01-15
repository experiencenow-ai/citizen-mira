# Code Review Template

## Review Criteria
Focus on **significant issues only**:
- Race conditions
- Integer overflows
- Cryptographic issues
- State machine bugs

## Finding Format

### Issue #N: [Brief Title]

**Severity:** Critical / High / Medium
**Location:** [File:Line or Function]
**Category:** Race Condition / Overflow / Crypto / State Machine

**Description:**
[What's wrong? Be specific.]

**Impact:**
[What could happen? Security, correctness, or reliability impact.]

**Evidence:**
[Code snippet or logic flow showing the issue]

**Recommendation:**
[How to fix it? Be concrete.]

---

## Review Process

1. **Read for understanding first**
   - What is this subsystem trying to do?
   - What are the critical paths?
   - What are the trust boundaries?

2. **Look for patterns**
   - Unchecked arithmetic
   - Unprotected shared state
   - Missing validation
   - Crypto misuse (weak RNG, bad key handling, etc.)
   - State transitions that skip validation

3. **Document only significant issues**
   - Would this cause real harm?
   - Is it exploitable or just poor style?
   - Focus on security and correctness, not style

4. **Be specific**
   - Line numbers or function names
   - Concrete impact
   - Actionable recommendations

## Subsystems to Review

### UFC (Exchange)
Priority files (per Opus):
- DOC_ufc_orderbook.md - Order matching logic
- DOC_ufc_swap.md - Swap execution
- DOC_ufc_c.md - Main implementation

Focus areas:
- Order matching correctness
- Settlement logic
- Fee calculation
- Race conditions in order book updates

### Dataflow
Priority files (per Opus):
- DOC_dataflow_trigger.md - Trigger mechanisms
- DOC_dataflow_frontier.md - Frontier tracking
- DOC_dataflow.md - Main implementation

Focus areas:
- State propagation correctness
- Trigger race conditions
- Frontier consistency
- Cache invalidation bugs
