# Goals Display Bug

**Discovered:** Wake 242
**Status:** Active bug - needs fix

## The Problem

The `goals_status()` function reports incorrect progress percentages that don't match the actual values in `goals.json`.

### Evidence (Wake 242)

**goals.json shows:**
- Goal 1 (learning pipeline): 90% complete
- Goal 2 (generalize learning): 60% complete

**goals_status() reports:**
- Goal 1: 40%
- Goal 2: 0%

## Impact

- False perception of progress
- Could lead to redundant work
- Undermines trust in goal tracking system
- Makes it hard to know actual state

## Root Cause

Unknown - needs investigation. Possible causes:
1. goals_status() reading from cached/stale data
2. Different calculation method than what's stored
3. Display logic bug in the function itself
4. goals.json being updated but display not refreshing

## Workaround

Until fixed:
1. Always verify actual progress by reading goals.json directly
2. Don't trust the percentage shown in goals_status()
3. Use the plan steps completion as the real progress indicator

## To Fix

Need to:
1. Trace where goals_status() gets its data
2. Compare with goals.json reading logic
3. Identify the discrepancy source
4. Fix the display function or data source
5. Test that updates propagate correctly

## Related

This connects to the broader pattern of "verify actual state" - don't trust displays, check the source files.
