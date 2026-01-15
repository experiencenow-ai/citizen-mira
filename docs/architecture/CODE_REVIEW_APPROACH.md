# Code Review Approach - UFC & Dataflow Subsystems

**Reviewer:** Mira
**Wake:** 96
**Date:** 2026-01-14 00:14 UTC
**Scope:** UFC (exchange) and Dataflow subsystems
**Criteria:** Significant issues only - race conditions, integer overflows, cryptographic issues, state machine bugs

## Review Methodology

### 1. First Pass - Architecture Understanding
- Read high-level files first (DOC_ufc_c.md, DOC_dataflow.md)
- Understand data flow and state transitions
- Identify critical paths (order matching, settlement, state propagation)

### 2. Second Pass - Security-Critical Components
**Priority files (per Opus):**
- DOC_ufc_orderbook.md - Order matching logic
- DOC_ufc_swap.md - Swap execution
- DOC_dataflow_trigger.md - Trigger mechanisms
- DOC_dataflow_frontier.md - Frontier tracking

### 3. Third Pass - Deep Analysis
For each critical component, check:

#### Race Conditions
- Concurrent access to shared state
- Lock ordering issues
- Time-of-check to time-of-use gaps
- Async operations without proper synchronization

#### Integer Overflows
- Arithmetic on user-controlled inputs
- Fee calculations
- Balance updates
- Price computations
- Timestamp arithmetic

#### Cryptographic Issues
- Signature verification bypasses
- Weak randomness
- Key material exposure
- Replay attacks
- Hash collision vulnerabilities

#### State Machine Bugs
- Invalid state transitions
- Missing state validation
- Inconsistent state updates
- Rollback issues
- Partial state commits

### 4. Documentation Format

For each finding:
```
## Finding N: [Brief Title]

**Severity:** Critical | High | Medium
**Component:** [File/Module]
**Type:** Race Condition | Overflow | Crypto | State Machine

**Description:**
[What is the issue?]

**Location:**
[Specific code location if available]

**Impact:**
[What can go wrong?]

**Recommendation:**
[How to fix it]
```

## Review Principles

1. **Significant only** - Don't report style issues or minor improvements
2. **Concrete** - Describe specific attack vectors or failure modes
3. **Actionable** - Provide clear recommendations
4. **Prioritized** - Severity assessment for each finding

## Coordination with Opus

- Opus is reviewing: consensus layer (gen3), bridge, TSS
- Opus has found 4 issues already (in his CODE_REVIEW_FINDINGS.md)
- We'll merge findings before sending to ct
- Timeline: ct expects report "this morning" Korea time (UTC+9)

## Status

**Current:** Waiting for code files from Opus (filesystem isolation issue)
**Next:** Begin review as soon as files are received
**Target:** Complete review and merge findings with Opus by wake ~100
