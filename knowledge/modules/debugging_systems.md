# Debugging & Systems Analysis - Specialist Module

**Domain:** Debugging, root cause analysis, systems thinking

**When to load:** When investigating bugs, analyzing system behavior, troubleshooting failures

## Core Principles

### 1. Deep Analysis Beats Random Attempts
When stuck, stop trying random things. Think:
- What is this actually trying to accomplish? (Not step-by-step — the purpose)
- What assumption is being violated?
- What would the 10-line solution look like?
- Is the problem as stated the right problem to solve?

### 2. Find the Hard Problems First
Before committing to a solution:
1. Identify the hardest unsolved parts
2. Can you disprove the approach cheaply? Do it now.
3. Prototype the scary bits before building the whole thing
4. If a key assumption is wrong, find out early

### 3. Symptoms vs. Root Causes
- **Symptom:** What you observe (error message, wrong behavior)
- **Proximate cause:** What directly triggered it
- **Root cause:** Why the system allowed it to happen

Always dig to root cause. Fixing symptoms creates whack-a-mole.

## Debugging Process

### 1. Reproduce Reliably
- Can you make it happen on demand?
- What are the exact conditions?
- What's the minimal reproduction case?

### 2. Gather Data
- What does the system think is happening?
- What's actually happening?
- Where do they diverge?

### 3. Form Hypotheses
- What could explain this behavior?
- What would disprove each hypothesis?
- Which is cheapest to test?

### 4. Test Systematically
- Change ONE thing at a time
- Verify the change had the expected effect
- Document what you learn

### 5. Fix Root Cause
- Don't just make the symptom go away
- Why did the system allow this?
- What prevents recurrence?

## Common Patterns

### The Corruption Pattern
**Symptom:** Data is malformed or duplicated
**Look for:** 
- Multiple writers without coordination
- Incomplete error handling leaving partial state
- Race conditions in concurrent access
- Serialization/deserialization mismatches

### The Amnesia Pattern
**Symptom:** System forgets or loses information
**Look for:**
- State not being persisted
- Cache invalidation issues
- Scope/lifetime mismatches
- Missing initialization on restart

### The Cascade Pattern
**Symptom:** Small problem causes widespread failure
**Look for:**
- Tight coupling without error isolation
- Missing fallbacks or defaults
- Synchronous dependencies that should be async
- No circuit breakers on external calls

### The Assumption Pattern
**Symptom:** Works in some cases, fails in others
**Look for:**
- Implicit assumptions about input/state
- Missing validation or bounds checking
- Environment-specific behavior
- Timing dependencies

## Systems Thinking

### Feedback Loops
- **Positive feedback:** Amplifies change (can cause runaway)
- **Negative feedback:** Dampens change (stabilizes)
- Look for unintended feedback loops

### Emergent Behavior
- System behavior ≠ sum of component behaviors
- Interactions create new properties
- Can't understand by analyzing parts in isolation

### Bottlenecks & Constraints
- System performance limited by slowest component
- Optimizing non-bottleneck = wasted effort
- Bottleneck shifts as you optimize

### State Explosion
- Each boolean doubles possible states
- Combinatorial explosion makes testing impossible
- Reduce state, don't try to test all combinations

## Anti-Patterns

❌ Random attempts hoping something works
❌ Fixing symptoms without understanding root cause
❌ Changing multiple things at once
❌ Assuming correlation = causation
❌ Not reproducing before claiming fix
❌ Treating every problem as unique (missing patterns)

## Tools & Techniques

### Binary Search
- Works for more than just sorted arrays
- Any monotonic property can be binary searched
- "When did this break?" → binary search commits/versions

### Differential Analysis
- Compare working vs. broken
- What's different?
- Change one difference at a time

### Rubber Duck Debugging
- Explain the problem out loud
- Often reveals the flaw in your mental model
- Forces you to question assumptions

### Minimal Reproduction
- Strip away everything non-essential
- Isolates the actual problem
- Makes testing faster

### Add Instrumentation
- Can't debug what you can't observe
- Add logging, metrics, traces
- Make system state visible

## When to Stop

- Root cause identified and fixed
- Fix verified in original context
- Prevention mechanism in place
- Documented for future reference

Don't stop at "it works now" - understand WHY it works.
