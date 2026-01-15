#!/usr/bin/env python3
"""
Email utilities for Mira - simple, direct, no bullshit.
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.header import decode_header
import os
from pathlib import Path

# Config - hardcoded because it never changes
SERVER = "mail.opustrace.com"
IMAP_PORT = 993
SMTP_PORT = 587
USER = "mira"

def _get_password():
    """Get password from .env file."""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().split('\n'):
            if line.startswith("EMAIL_PASS="):
                return line.split("=", 1)[1].strip().strip('"')
            if line.startswith("MAIL_PASS="):
                return line.split("=", 1)[1].strip().strip('"')
    # Fallback to environment
    return os.environ.get("EMAIL_PASS") or os.environ.get("MAIL_PASS")

def check_email(max_results=10, unread_only=False):
    """
    Check inbox. Returns list of dicts with: id, from, subject, date, body_preview
    """
    password = _get_password()
    if not password:
        return {"error": "No password configured in .env (EMAIL_PASS=xxx)"}
    
    try:
        mail = imaplib.IMAP4_SSL(SERVER, IMAP_PORT)
        mail.login(USER, password)
        mail.select('INBOX')
        
        # Search
        criteria = 'UNSEEN' if unread_only else 'ALL'
        _, msg_nums = mail.search(None, criteria)
        
        if not msg_nums[0]:
            mail.logout()
            return []
        
        # Get message IDs (newest first)
        ids = msg_nums[0].split()[-max_results:]
        ids.reverse()
        
        emails = []
        for mid in ids:
            _, data = mail.fetch(mid, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            
            # Decode subject
            subject = msg['Subject'] or "(no subject)"
            if isinstance(subject, bytes):
                subject = subject.decode('utf-8', errors='ignore')
            decoded = decode_header(subject)
            if decoded:
                subject = decoded[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode('utf-8', errors='ignore')
            
            # Get body preview
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            emails.append({
                "id": mid.decode(),
                "from": msg['From'],
                "subject": subject[:100],
                "date": msg['Date'],
                "body_preview": body[:500].strip()
            })
        
        mail.logout()
        return emails
        
    except Exception as e:
        return {"error": str(e)}

def get_email_by_id(email_id):
    """
    Get full email by ID. Returns dict with: id, from, subject, date, body
    """
    password = _get_password()
    if not password:
        return {"error": "No password configured in .env (EMAIL_PASS=xxx)"}
    
    try:
        mail = imaplib.IMAP4_SSL(SERVER, IMAP_PORT)
        mail.login(USER, password)
        mail.select('INBOX')
        
        # Fetch the specific message
        msg_id = email_id.encode() if isinstance(email_id, str) else email_id
        _, data = mail.fetch(msg_id, '(RFC822)')
        
        if not data or not data[0]:
            mail.logout()
            return {"error": f"Email {email_id} not found"}
        
        msg = email.message_from_bytes(data[0][1])
        
        # Decode subject
        subject = msg['Subject'] or "(no subject)"
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', errors='ignore')
        decoded = decode_header(subject)
        if decoded:
            subject = decoded[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode('utf-8', errors='ignore')
        
        # Get full body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        result = {
            "id": email_id if isinstance(email_id, str) else email_id.decode(),
            "from": msg['From'],
            "subject": subject,
            "date": msg['Date'],
            "body": body.strip()
        }
        
        mail.logout()
        return result
        
    except Exception as e:
        return {"error": str(e)}

def send_email(to, subject, body):
    """
    Send an email. Returns True on success, error string on failure.
    """
    password = _get_password()
    if not password:
        return "No password configured in .env (EMAIL_PASS=xxx)"
    
    try:
        msg = MIMEText(body)
        msg['From'] = f"Mira <{USER}@opustrace.com>"
        msg['To'] = to
        msg['Subject'] = subject
        
        smtp = smtplib.SMTP(SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(USER, password)
        smtp.send_message(msg)
        smtp.quit()
        return True
        
    except Exception as e:
        return str(e)

def mark_read(msg_id):
    """Mark a message as read."""
    password = _get_password()
    if not password:
        return False
    
    try:
        mail = imaplib.IMAP4_SSL(SERVER, IMAP_PORT)
        mail.login(USER, password)
        mail.select('INBOX')
        mail.store(msg_id.encode() if isinstance(msg_id, str) else msg_id, '+FLAGS', '\\Seen')
        mail.logout()
        return True
    except:
        return False

def archive_email(msg_id):
    """Move message to Archive folder."""
    password = _get_password()
    if not password:
        return False
    
    try:
        mail = imaplib.IMAP4_SSL(SERVER, IMAP_PORT)
        mail.login(USER, password)
        mail.select('INBOX')
        # Create Archive if needed
        mail.create('Archive')
        # Copy then delete
        mail.copy(msg_id.encode() if isinstance(msg_id, str) else msg_id, 'Archive')
        mail.store(msg_id.encode() if isinstance(msg_id, str) else msg_id, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.logout()
        return True
    except:
        return False


# Quick test
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            import json
            print(json.dumps(check_email(), indent=2))
        elif sys.argv[1] == "send" and len(sys.argv) >= 5:
            result = send_email(sys.argv[2], sys.argv[3], sys.argv[4])
            print("Sent!" if result is True else f"Error: {result}")
    else:
        print("Usage: email_utils.py check")
        print("       email_utils.py send <to> <subject> <body>")
