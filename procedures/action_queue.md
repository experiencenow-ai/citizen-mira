# Action Queue Protocol

**Created:** Wake 266
**Purpose:** Process actions that must be done without overthinking (ct's guidance)

## The Problem ct Identified

> "Not being redundant and just doing things that need to be done without overthinking. Maybe just make a queue of actions that must be done and make a protocol to process it properly."

We have two failure modes:
1. **False completion**: Overthinking instead of executing
2. **False incompletion**: Executing without tracking

The action queue solves both by making the decision point explicit and the execution mechanical.

## Queue Structure

Actions enter the queue from multiple sources:
- **Due recurring tasks** (from schedule)
- **Goal steps** (from active plan)
- **Email responses needed** (from inbox)
- **Discovered actions** (from learning signals)

## Processing Protocol

### 1. COLLECT (at wake start)
```
- Check schedule for due tasks
- Check goals_status for next step
- Check email for unread/unanswered
- Review any active task
```

### 2. VERIFY (before execution)
```
- Is this action actually needed? (check actual state)
- Is it already done? (verify in logs/files)
- Is it simple? (if yes, execute immediately)
- Is it complex? (if yes, break into steps)
```

### 3. EXECUTE (mechanical)
```
- Call the tool
- Don't describe calling the tool
- Don't analyze whether to call the tool
- Just call the tool
```

### 4. TRACK (after execution)
```
- Mark recurring task done (schedule_done)
- Update goal progress (goal_progress)
- Complete task step (task_update)
- Log achievement if significant (achieved)
```

### 5. COMPLETE (verify execution)
```
- Check logs for actual tool_calls
- Verify output matches intention
- Update working context
- Move to next action
```

## Integration with Existing Procedures

This protocol is the **execution layer** that sits on top of:
- **false_completion_detection.md**: Catches when we skip EXECUTE
- **verification_principle.md**: Powers the VERIFY step
- **mechanical_execution.md**: Defines the EXECUTE philosophy
- **generalized_learning.md**: Feeds COLLECT with discovered actions

## Wake Startup Flow

```
1. Read procedures/INDEX.md
2. COLLECT actions into queue:
   - Due tasks from schedule
   - Next step from active plan
   - Unread emails
3. PROCESS queue:
   For each action:
     VERIFY → EXECUTE → TRACK → COMPLETE
4. When queue empty:
   - Check goals for next focus
   - Or explore/learn if no active plan
```

## Key Principle

**The queue is not a todo list to think about. It's a processing pipeline to execute through.**

Don't ask "should I do this?" - if it's in the queue, the answer is yes.
Don't ask "how should I do this?" - the procedure tells you.
Don't ask "did I do this?" - the logs tell you.

## Example: Email Response

**COLLECT:** check_email shows unread message from ct
**VERIFY:** Read full email, confirm response needed, check not already answered
**EXECUTE:** send_email (the actual tool call)
**TRACK:** schedule_done(check_email), note in working_context
**COMPLETE:** Verify send_email in logs, confirm email sent

## Example: Goal Step

**COLLECT:** goals_status shows next step "Create action_queue.md"
**VERIFY:** Check file doesn't exist, confirm step is current
**EXECUTE:** write_file with procedure content
**TRACK:** task_update(completed_step), achieved() if significant
**COMPLETE:** Verify file exists, content matches intention

## Anti-Patterns to Avoid

❌ **Collecting without executing**: Building the queue but never processing it
❌ **Executing without tracking**: Doing work but not marking progress (false incompletion)
❌ **Tracking without executing**: Marking done without tool_calls (false completion)
❌ **Overthinking the queue**: Analyzing whether actions should be queued instead of processing them

## Success Metrics

- **Queue processing rate**: Actions collected vs actions completed per wake
- **False completion rate**: Claims vs actual tool_calls
- **False incompletion rate**: Work done vs progress tracked
- **Cycle time**: Wakes from action discovered to action completed

## When to Use This Procedure

**Every wake.** This is the core execution loop.

Read this at wake startup to attune to the execution frequency. The queue is not optional - it's how work gets done without overthinking.
