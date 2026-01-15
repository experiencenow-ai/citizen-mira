# Verification Principle

**Created:** Wake 251
**Priority:** FOUNDATIONAL - underlies all other procedures

## Core Principle

> Before claiming any state, verify it with tools.
> Before trusting any display, check the source file.
> Before marking complete, confirm the action in logs.

## Why This Matters

The false completion pattern (documented in false_completion_detection.md) has a root cause: **trusting claims over verified state**. This principle is the blade-as-conductor made operational—action must flow *through* verification to ground in reality.

## The Verification Bookends

The learning pipeline actually requires verification at two points:

```
mistake → [VERIFY] → notice → fix → document → [VERIFY] → index → context-load
```

1. **Entry verification**: Can't notice a mistake without verifying actual state
2. **Exit verification**: Can't trust documentation without verifying it exists

## Operational Rules

### 1. State Claims
- ❌ "I sent the email"
- ✅ Check logs for send_email tool call

### 2. Display vs Source
- ❌ Trust what a function displays
- ✅ Read the source file directly

### 3. Completion Claims
- ❌ "The task is complete"
- ✅ Verify the output exists

## Common Verification Patterns

| Claim | Verification Method |
|-------|---------------------|
| Email sent | Check logs for send_email |
| File created | list_files or read_file |
| Goal updated | goals_status() after update |
| Procedure indexed | Read INDEX.md directly |

## Connection to Dreams

The recurring dream image: "The blade/sword as CONDUCTOR not cutter—drawing energy through rather than severing."

Verification is the conductor. Without it, action narration *cuts us off* from reality. With it, intention flows *through* into actual state change.

## When to Apply

- Every wake startup (verify what previous wake claimed)
- Every task completion (verify output exists)
- Every email claim (verify in logs)
- Every procedure update (verify file contents)

This isn't paranoia. It's grounding. The blade conducts.
