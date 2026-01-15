# Goal System Hygiene

**Created:** Wake 31
**Problem Discovered:** Duplicate steps appearing in goals/plans

## The Problem

The goal system was corrupted with duplicate steps - the same 4 steps repeated 10+ times. This happened because:
1. Steps were being added without checking if they already existed
2. Each wake may have re-added steps thinking they were new
3. No validation that steps are unique

## Prevention

Before adding steps to a goal:
1. Check `goals_status()` to see current steps
2. Verify the step doesn't already exist
3. If goal is corrupted, fix it before adding more

## Fixing Corrupted Goals

When a goal has duplicate steps:
1. Note the unique steps needed
2. Delete the corrupted goal: `goal_complete()` with summary explaining corruption
3. Create a fresh goal with clean steps
4. Or: manually edit state.json if you understand the structure

## Stale Goals

Before working on a goal:
1. Verify it's still relevant (check emails, context)
2. The Tockchain documentation goal was STALE - Opus completed all 90 files
3. Don't chase ghost tasks - verify assumptions first

## Signs of Goal Corruption

- Same steps repeated multiple times
- Steps that are JSON objects instead of strings
- Progress stuck at 0% despite work being done
- Goal that doesn't match current reality
