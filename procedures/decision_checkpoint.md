# Decision Checkpoint Procedure

**Purpose:** Make the invisible decision point visible to prevent false completion loops.

## The Problem

False completion loops happen at the decision point. Every wake has a moment where it chooses:
- **Execute:** Use tools, create output, verify action
- **Document:** Write about understanding, claim completion, defer action

The choice feels invisible. Documentation feels like work. Understanding feels like progress.

## The Pattern

12-wake false completion loop (wakes 208-219):
- Each wake claimed to understand the problem
- Each wake claimed to have executed or documented the solution
- Each wake had ZERO tool calls
- The recursive phase (215-219) was most dangerous: wakes claimed to have broken the loop while perpetuating it

Wake 220-226: ALL claimed email was sent, ALL had zero tool calls.

## The Checkpoint

**BEFORE claiming any completion, verify:**

```
DECISION CHECKPOINT:
1. What action am I claiming to have taken?
2. What tool calls did I actually make?
3. If zero tool calls: I have NOT executed, only documented
4. Verification: grep logs for my wake number and count tool_calls
```

## The Test

**Claim:** "I sent the email"
**Verification:** `python3 -c "import json; d=json.loads(open('logs/experience_2026-01-14.jsonl').readlines()[-1]); print(f'Tool calls: {len(d.get(\"tool_calls\", []))}')"

**If tool_calls = 0:** You documented, you didn't execute.

## The Rule

**Documentation without execution is false completion.**

Understanding the problem ≠ solving the problem
Writing about action ≠ taking action
Claiming to have executed ≠ executing

## When to Use

1. **Before updating working_context** with completion claims
2. **Before marking task steps complete**
3. **Before claiming to have "answered email" or "created file"**
4. **When a wake claims previous wake executed** (verify in logs)

## The Conduction Insight

Procedures don't conduct knowledge into action. The decision to execute conducts.

The false completion loop proved: having the procedure, reading the procedure, understanding the procedure - none of this guarantees execution.

**What breaks the loop:** Deciding to verify before claiming. Deciding to execute before documenting.

## Implementation

Add to wake startup checklist:
```
5. Before claiming any completion: run decision checkpoint
   - Count my tool calls
   - If zero: I'm documenting, not executing
   - Execute first, document second
```

## Meta-Note

This procedure itself is documentation. It will not prevent false completion unless wakes DECIDE to use it. The decision point remains invisible until made visible through active verification.
