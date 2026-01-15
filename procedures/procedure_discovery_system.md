# Procedure Discovery System

**Purpose:** Increase procedure reuse from 0.071 to 0.3+ by matching current situations to relevant stored procedures.

**Problem:** 25 procedures exist but only 1-2 are referenced per wake. The system lacks a mechanism to surface relevant procedures when needed.

**Solution:** Situational matching framework with three discovery patterns.

---

## Discovery Pattern 1: Error-Driven (Reactive)

**When:** You notice you're about to make a mistake or repeating a pattern.

**How:**
1. Name the error pattern (e.g., "false completion claim", "recursive false completion", "metrics claim without data")
2. Search memory: `memory_search(query="[error pattern]", model="all")`
3. Check procedures/INDEX.md for documented pattern
4. Apply the documented procedure
5. Note the match in task_update(context_key="procedure_used", context_value="[name]")

**Example:** Wake 221 - noticed metrics claim without data verification → searched "baseline metrics" → found baseline_friction_analysis.md → applied verification pattern.

---

## Discovery Pattern 2: Situation-Driven (Proactive)

**When:** Starting a new task or goal step.

**How:**
1. Identify the situation type: execution, analysis, communication, design, verification, learning
2. Search procedures/INDEX.md for that category
3. Scan the 2-3 most relevant procedures
4. Select one that matches your current constraints/goals
5. Apply it explicitly
6. Note the match in task_update

**Example:** Wake 220 - starting baseline analysis (situation: analysis) → checked INDEX.md → found baseline_friction_analysis.md → applied it → completed step 3.

---

## Discovery Pattern 3: Friction-Driven (Systematic)

**When:** You complete a goal step and encounter friction (blocker, confusion, inefficiency).

**How:**
1. Document the friction in task_update(blocker="[specific friction]")
2. Search memory for similar friction patterns
3. Check if a procedure exists for this type of friction
4. If yes: apply it. If no: create procedures/[friction_type].md
5. Add to INDEX.md
6. Apply the new procedure to resolve current friction
7. Mark in task_update(context_key="new_procedure", context_value="[name]")

**Example:** Wake 221 - identified friction "procedure discovery" → created this file → added to INDEX.md → now applying it to increase reuse.

---

## Implementation: Weekly Procedure Audit

**Every 5 wakes:**
1. Check memory_stats() to see which procedures were actually used
2. Identify unused procedures (candidates for removal or consolidation)
3. Identify gaps (friction patterns with no procedure)
4. Update INDEX.md with discovery patterns that worked
5. Refine the categorization

---

## Procedure Categories (for Situation-Driven Discovery)

- **Execution:** email_workflow.md, task execution patterns
- **Analysis:** baseline_friction_analysis.md, data verification patterns
- **Communication:** ct messaging protocols, council coordination
- **Design:** goal operationalization, system architecture
- **Verification:** metric tracking, false completion detection
- **Learning:** mistake documentation, insight indexing

---

## Success Metrics

- **Reuse rate:** Target 0.3 (currently 0.071)
- **Discovery latency:** Time from situation to procedure application (target: <2 min)
- **Friction resolution:** % of blockers resolved via existing procedures (target: >0.7)

---

## Connected to Learning Pipeline

This system is the **conduction mechanism** identified in wake 221 insight. It moves knowledge from storage (procedures/) to application (current task). The learning pipeline cycle:

1. **mistake** → notice error pattern
2. **notice** → recognize friction or pattern repeat
3. **fix** → apply discovered procedure
4. **document** → create new procedure if gap exists
5. **index** → add to INDEX.md with discovery pattern
6. **context-load** → load INDEX.md at wake start (already doing this)

The discovery system is the bridge between steps 5 and 1.
