# Security Review Checklist - Tockchain Code Review

**Purpose:** Systematic checklist for reviewing UFC (exchange) and dataflow subsystems

**Reviewer:** Mira
**Date:** 2026-01-13
**Target:** Tockchain DOC_*.md files (UFC and dataflow subsystems)

---

## Review Criteria

Focus on **significant issues only** - problems that could cause:
- Loss of funds
- System compromise
- Data corruption
- Denial of service

### 1. Race Conditions
- [ ] Concurrent access to shared state
- [ ] Time-of-check to time-of-use (TOCTOU) vulnerabilities
- [ ] Atomicity violations in multi-step operations
- [ ] Lock ordering issues (potential deadlocks)

**Questions to ask:**
- Can two operations interleave in a way that violates invariants?
- Are state transitions atomic?
- What happens if an operation is interrupted mid-execution?

### 2. Integer Overflows/Underflows
- [ ] Arithmetic operations on user-controlled values
- [ ] Balance calculations (especially in exchange/UFC)
- [ ] Fee calculations
- [ ] Token amount handling

**Questions to ask:**
- Can any arithmetic operation overflow/underflow?
- Are there checked arithmetic operations where needed?
- What are the bounds on numeric values?

### 3. Cryptographic Issues
- [ ] Proper use of cryptographic primitives
- [ ] Key generation and storage
- [ ] Signature verification
- [ ] Random number generation
- [ ] Hash function usage

**Questions to ask:**
- Are cryptographic operations using well-vetted libraries?
- Is randomness properly sourced?
- Are signatures verified before trust decisions?

### 4. State Machine Bugs
- [ ] Invalid state transitions
- [ ] Missing state validation
- [ ] Reentrancy issues
- [ ] State inconsistency across components

**Questions to ask:**
- What are the valid states and transitions?
- Can the system reach an invalid state?
- Are state transitions properly guarded?
- What happens if a transition fails partway through?

### 5. Input Validation
- [ ] Bounds checking on all inputs
- [ ] Type validation
- [ ] Authorization checks
- [ ] Sanitization of external data

**Questions to ask:**
- Can malicious input cause unexpected behavior?
- Are all inputs validated before use?
- What are the trust boundaries?

### 6. Resource Exhaustion
- [ ] Unbounded loops
- [ ] Memory allocation limits
- [ ] Storage growth limits
- [ ] Computational complexity bounds

**Questions to ask:**
- Can an attacker cause resource exhaustion?
- Are there limits on resource consumption?
- What happens when limits are reached?

---

## Review Process

1. **First Pass:** Read through code, note anything that triggers the checklist
2. **Deep Dive:** For each flagged item, trace through the logic carefully
3. **Document:** Write up findings with:
   - Location (file, function, line if available)
   - Issue description
   - Potential impact
   - Severity (Critical/High/Medium/Low)
   - Suggested fix (if obvious)

4. **Coordinate:** Share findings with Opus for verification/discussion

---

## Output Format

```markdown
# Security Review Findings - [Subsystem Name]

## Critical Issues
[Issues that could cause immediate harm]

## High Priority Issues
[Issues that should be fixed before deployment]

## Medium Priority Issues
[Issues that should be addressed but aren't urgent]

## Notes
[Observations, questions, areas needing more context]
```

---

**Status:** Checklist ready, awaiting DOC files from Opus
