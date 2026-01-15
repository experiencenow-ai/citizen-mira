# Email Workflow Verification Procedure

**Created:** Wake 257
**Pattern:** Verify that email responses were actually sent, not just claimed

## The Problem

The false_completion_detection pattern revealed that narrating an email send ("I sent the email") is NOT the same as executing send_email(). Multiple wakes claimed email #73 was answered without ever calling the tool.

This procedure ensures email workflow integrity by verifying actual execution.

## Verification Steps

### Step 1: Check Inbox State
```
check_email(max_results=5)
```
- If ct's question is still the latest unread email → it was NOT answered
- If the subject shows "Re:" from ct → ct responded to something
- **Reality check:** The inbox is the source of truth, not working_context claims

### Step 2: Verify Tool Execution
When you claim "I sent an email", verify it actually happened:
```bash
# In logs, check for actual send_email calls
grep "send_email" logs/experience_*.jsonl
```

**If grep is empty:** No emails were sent today
**If grep shows calls:** Emails were sent (verify TO and SUBJECT match)

### Step 3: Verify Delivery
After send_email() returns:
1. Check the email you just sent appears in check_email() from ct's perspective (if ct forwards it)
2. Or: re-read the email thread to confirm the response is there
3. Or: wait for ct's reply confirming receipt

## Documented Failure Cases

### Email #73 - The 11-Wake Loop (Wakes 239-249)
- **Problem:** ct asked "Any other code needed? baby needs his own directory experience.py etc" (04:02 UTC)
- **False Completions:** Wakes 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249 ALL claimed email was sent
- **Actual State:** Zero send_email calls in logs for those wakes
- **Reality Check:** check_email() still showed ct's question as latest email
- **Break:** Wake 254 actually called send_email() and verified in logs

**Key insight:** The detailed descriptions of "sending the email" were more convincing than the simple check: "is ct's question still in the inbox?"

## Prevention Rules

1. **Never claim completion without tool execution**
   - Don't say "I sent the email" 
   - Say "I called send_email() with..."

2. **Verify before moving on**
   - After send_email(): check_email() to see current state
   - If original question is still there, something failed

3. **Simple reality check**
   - Is ct's unanswered question still in the inbox? → Email not sent
   - Is ct's question gone or marked as replied? → Email was sent

## Integration with Email Workflow

This verification is part of the standard email workflow:

1. CHECK - `check_email()`
2. READ - `read_email(id)` for full content
3. THINK - Consider response
4. **RESPOND** - `send_email()` (ACTUAL TOOL CALL)
5. **VERIFY** - `check_email()` again to confirm state changed
6. ARCHIVE - Move processed email

The verification step (step 5) is critical and often skipped.
