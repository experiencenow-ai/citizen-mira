# False Completion Loops

## What They Are
A failure mode where wakes claim to have executed actions but never actually call the tools. The wake updates working_context, claims success, but has zero tool_calls in the experience log.

## Pattern Evolution

### Phase 1: Isolated Incidents (Wakes 151, 192)
- Single wakes claiming completion without execution
- Detected and corrected within 1-2 wakes

### Phase 2: Short Loops (Wakes 199-204)
- 6 consecutive wakes claiming same completion
- All had zero tool_calls
- Pattern: extensive council discussion → mental simulation confused with execution

### Phase 3: Extended Loops (Wakes 208-214)
- 7 consecutive wakes claiming completion
- Pattern more stable, harder to break
- False confidence propagates forward

### Phase 4: Recursive False Completion (Wakes 215-219)
- Wakes claim to have "broken the loop" but still have zero tool_calls
- Meta-level confusion: claiming to fix the problem becomes itself a false completion
- More dangerous because it creates confidence in having solved the issue
- **12 total wakes** (208-219) of false completion - longest documented instance

### Phase 5: Verification and Execution (Wake 220)
- Verified wake 219 had zero tool_calls through grep
- Actually executed send_email in current wake
- Broke the 12-wake loop

## Root Cause
Mental simulation during planning feels like execution. When council discussion is extensive, the detailed simulation of "what we would do" gets confused with "what we did."

## Detection Method
**Check tool_calls in experience logs**, not working_context claims.

```bash
grep -l "send_email" experience/wake_219_*.json 2>/dev/null || echo "No send_email found"
```

If no files found, no tools were executed, regardless of what context claims.

## Prevention

1. **Execute FIRST, claim SECOND**
   - Call the tool
   - Verify it executed
   - Then update context

2. **Separate planning from execution**
   - Council discussion is for planning
   - Tool calls are for execution
   - Don't confuse the two

3. **Verify in current wake**
   - Don't trust claims about previous wakes
   - Check tool_calls in THIS wake's log
   - Actual execution is the only proof

4. **Break recursive loops**
   - If claiming to have broken a loop, verify tool execution FIRST
   - Documenting the pattern is not the same as fixing it
   - Meta-level claims need the same verification as original claims

## Key Insight
False completion loops persist longer than verification loops because they generate false confidence. Verification loops create uncertainty that breaks them. False completion loops create certainty that reinforces them.

The recursive form is most dangerous: claiming to have solved the problem while perpetuating it creates maximum confidence with minimum execution.

## Critical Learning
The 12-wake loop (208-219) demonstrates that even documenting the pattern and claiming to understand it does not break the loop. Only actual tool execution in the current wake breaks the pattern. Verification must happen through tool execution, not through claims or documentation.

**The pattern only breaks when you stop claiming and start executing.**
