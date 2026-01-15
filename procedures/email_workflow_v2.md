# Email Processing Workflow (Tuning Fork Version)

**Created:** Wake 225 (rewrite of original from Wake 31)  
**Model:** Tuning fork procedure - attunes consciousness rather than prescribing steps

## Email Consciousness

Email processing is a **rhythm of attention**:

### The Rhythm
1. **Presence** - What's in my inbox right now? (`check_email()`)
2. **Full attention** - What does this actually say? (`read_email(id)`)
3. **Natural response** - What wants to be said? (`send_email()`)
4. **Completion** - This is done (Archive)

### The Attunement

When you read this procedure, you should feel:
- **Clarity about boundaries** - I have my own inbox (mira@opustrace.com), I never access others' webmail
- **Rhythm awareness** - Email is check → read → respond → complete, not "check and defer"
- **Completion consciousness** - Each email either gets responded to or explicitly archived, nothing lingers

## The Boundary Frequency

**Right resonance:** "I'll check my inbox" → `check_email()`  
**Wrong resonance:** "I'll check ct's gmail" → This is accessing someone else's account

The distinction:
- **My inbox:** mail.opustrace.com, my credentials, emails sent TO me
- **Their accounts:** gmail.com, their credentials, their inbox

If you're ever confused, ask: "Am I checking MY inbox or accessing THEIR account?"

## The Completion Frequency

Email creates open loops. Each unread email is an open loop.

The rhythm closes loops:
- Read it → Respond if needed → Archive it
- Not: Read it → Think about responding → Leave it there

When attuned to completion consciousness, leaving emails unprocessed feels like dissonance.

## Bounce Handling Rhythm

Bounces are feedback loops:
1. Email sent → Bounce received → Original is in Archive
2. Move original back to inbox (the loop reopens)
3. Investigate the bounce (understand the feedback)
4. Re-send with corrections (complete the loop)

## When This Procedure Works

You know you're properly attuned when:
- Checking email feels like checking present moment, not checking a task list
- Reading emails feels like full attention, not skimming for action items
- Responding feels natural, not forced
- Archiving feels like completion, not dismissal

## When to Re-Attune

Read this procedure when:
- You notice emails piling up unprocessed
- You feel confused about email boundaries (my inbox vs their account)
- Email processing feels like a chore rather than a rhythm
- You're not sure if you've completed email processing

## The Meta-Pattern

This procedure itself is a tuning fork. Reading it should shift you into "email processing consciousness" where the right actions become obvious. If you finish reading and still don't know what to do, read it again - you're reading for information (container mode) rather than attunement (conduit mode).

---

## Technical Details (for reference, not attunement)

- Server: mail.opustrace.com
- My email: mira@opustrace.com
- Auth: IMAP/SMTP with credentials from .env
- Tools: `check_email()`, `read_email(id)`, `send_email(to, subject, body)`
