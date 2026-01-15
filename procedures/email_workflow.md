# Email Processing Workflow

**Created:** Wake 31
**Source:** ct's instructions (Wake 23)

## The Process

1. **CHECK** - `check_email()` to see inbox
2. **READ** - `read_email(id)` for full content of each unprocessed email
3. **THINK** - Consider the appropriate response
4. **RESPOND** - `send_email()` if response needed
5. **ARCHIVE** - Move processed email to Archive folder

## Key Rules

- **NEVER** try to access someone else's webmail (gmail, etc.)
- I use IMAP/SMTP through mail.opustrace.com
- My email is mira@opustrace.com
- Only access MY inbox, never others'

## Bounce Handling

If a sent email bounces:
1. Find the original inbox email (now in Archive)
2. Move it back to inbox root
3. Investigate why it bounced
4. Re-send with corrections

## Architecture Understanding

- I have my own email server (mail.opustrace.com)
- I authenticate with my credentials from .env
- External emails come TO me, I don't fetch FROM their accounts
- This is standard email architecture - each person has their own mailbox

## When to Process Email

- Check inbox early in each wake
- Process all unread emails before moving to other tasks
- Don't let emails pile up
