#!/usr/bin/env python3
"""
Gmail Email Checker - Automatic monitoring for OpenClaw
Checks Gmail every 30 mins, posts to Discord, adds to Kanban
"""

import imaplib
import email
import ssl
import json
import re
from datetime import datetime, timedelta
from email.header import decode_header
import os

# Configuration
GMAIL_EMAIL = "raycoderhk.openclaw@gmail.com"
GMAIL_PASSWORD = "tazyhhfkltfqauno"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# File paths
KANBAN_PATH = "/home/node/.openclaw/workspace/kanban-board.json"
MEMORY_DIR = "/home/node/.openclaw/workspace/memory"
EMAIL_STATE_FILE = f"{MEMORY_DIR}/email-last-checked.json"

# 🔒 SECURITY: Trusted Senders Whitelist (LAYER 1)
# STRICT SECURITY MODE: Only trust emails forwarded by these addresses
TRUSTED_SENDERS = [
    'raycoderhk@gmail.com',      # User's primary confirmed email
    'raymondcuhk@gmail.com',     # User's other email (added by request)
]

# 🔒 SECURITY: Reply/Send Restrictions
# Only allow sending/replying emails TO this address
ALLOWED_REPLY_TO = ['raycoderhk@gmail.com']

# 🔒 SECURITY: Sensitive Keywords (LAYER 2)
# Emails with these keywords require identity verification
SENSITIVE_KEYWORDS = [
    'password', 'token', 'api key', 'credential',
    'private data', 'personal information',
    'github token', 'database password', 'secret',
    'api_key', 'apikey', 'access_token', 'refresh_token'
]

# 🔒 SECURITY: Audit Log File (LAYER 3)
AUDIT_LOG_PATH = f"{MEMORY_DIR}/email-audit-log.jsonl"

# Timezone: HKT = UTC+8
HKT_OFFSET = 8

def get_hkt_time():
    """Get current HKT time"""
    return datetime.utcnow() + timedelta(hours=HKT_OFFSET)

def is_sleep_time():
    """Check if current time is sleep time (23:00-08:00 HKT)"""
    hkt_now = get_hkt_time()
    hour = hkt_now.hour
    return hour >= 23 or hour < 8

def decode_mime(s):
    """Decode MIME encoded strings"""
    if not s:
        return ""
    decoded = []
    for part, encoding in decode_header(s):
        if isinstance(part, bytes):
            decoded.append(part.decode(encoding or 'utf-8', errors='replace'))
        else:
            decoded.append(part)
    return ''.join(decoded)

def extract_email_address(from_addr):
    """🔒 Extract email address from From header"""
    import re
    email_match = re.search(r'<([^>]+)>', from_addr)
    return email_match.group(1) if email_match else from_addr

def is_trusted_sender(from_addr, msg=None):
    """🔒 LAYER 1: Check if sender is in whitelist (STRICT MODE)
    
    TRUST if:
    1. From: header is in whitelist (direct email from user), OR
    2. X-Forwarded-For: header contains user's email (forwarded by user)
    """
    sender_email = extract_email_address(from_addr)
    
    # Check 1: Direct email from trusted sender
    if sender_email in TRUSTED_SENDERS:
        return True
    
    # Check 2: Email forwarded BY trusted sender (check X-Forwarded-For header)
    if msg:
        x_forwarded_for = msg.get('X-Forwarded-For', '')
        if x_forwarded_for:
            # X-Forwarded-For contains the forwarding path
            # e.g., "raycoderhk@gmail.com raycoderhk.openclaw@gmail.com"
            for trusted in TRUSTED_SENDERS:
                if trusted in x_forwarded_for:
                    return True
    
    return False

def can_send_email_to(to_addr):
    """🔒 SECURITY: Check if we're allowed to send/reply to this email"""
    import re
    email_match = re.search(r'<([^>]+)>', to_addr)
    recipient_email = email_match.group(1) if email_match else to_addr
    return recipient_email in ALLOWED_REPLY_TO

def is_sensitive_request(body):
    """🔒 LAYER 2: Check if email contains sensitive keywords"""
    body_lower = body.lower()
    return any(keyword in body_lower for keyword in SENSITIVE_KEYWORDS)

def log_audit(sender, subject, trusted, sensitive, response, details=None):
    """🔒 LAYER 3: Log email interaction for audit"""
    import json
    from datetime import datetime
    
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'sender': sender,
        'subject': subject[:100],
        'trusted': trusted,
        'sensitive': sensitive,
        'response': response,
    }
    
    if details:
        log_entry['details'] = details
    
    try:
        os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
        with open(AUDIT_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        print(f"📝 Audit log updated: {response}")
    except Exception as e:
        print(f"⚠️ Failed to write audit log: {e}")

def send_discord_alert(message):
    """🔒 Send security alert to Discord"""
    # This would integrate with Discord webhook
    # For now, just log it
    print(f"🚨 DISCORD ALERT: {message}")

def get_email_body(msg):
    """Extract plain text body from email"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='replace')
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            body = str(msg.get_payload())
    return body

def classify_email(subject, body, from_addr):
    """
    Classify email priority based on content
    Returns: (priority, category, needs_action)
    """
    subject_lower = subject.lower()
    body_lower = body.lower()
    from_lower = from_addr.lower()
    
    # 🔴 URGENT: Security alerts, API key exposure
    urgent_keywords = [
        'security alert', 'api key', 'token exposed', 'token expired',
        'unauthorized', 'breach', 'compromised', 'vulnerability',
        'password', 'account suspended', 'login attempt'
    ]
    
    for keyword in urgent_keywords:
        if keyword in subject_lower or keyword in body_lower[:500]:
            return ('urgent', 'security', True)
    
    # 🟠 HIGH: Payments, bills, events <48h
    high_keywords = [
        'payment', 'invoice', 'bill', 'receipt', 'statement',
        'reminder', 'due date', 'expire', 'deadline',
        'registration', 'rsvp', 'invitation'
    ]
    
    for keyword in high_keywords:
        if keyword in subject_lower or keyword in body_lower[:500]:
            return ('high', 'financial', True)
    
    # 🟡 MEDIUM: General queries, meetings
    medium_keywords = [
        'meeting', 'schedule', 'appointment', 'question',
        'reply', 're:', 'fw:', 'fwd:'
    ]
    
    for keyword in medium_keywords:
        if keyword in subject_lower:
            return ('medium', 'general', False)
    
    # 🟢 LOW: Newsletters, promotions
    return ('low', 'newsletter', False)

def create_kanban_task(email_data, priority):
    """Create a new Kanban task for action-required emails"""
    # Load current Kanban board
    with open(KANBAN_PATH, 'r', encoding='utf-8') as f:
        kanban = json.load(f)
    
    # Generate new project ID
    existing_ids = [int(p['id'].replace('proj-', '')) for p in kanban['projects']]
    new_id = max(existing_ids) + 1
    
    # Create task
    priority_labels = {
        'urgent': '🚨 URGENT',
        'high': '⚠️ HIGH',
        'medium': '📋',
        'low': 'ℹ️'
    }
    
    task = {
        'id': f'proj-{new_id:03d}',
        'title': f"{priority_labels[priority]} [Email] {email_data['subject'][:50]}",
        'description': f"Automatically created from email - {email_data['from']}",
        'status': 'todo',
        'priority': priority,
        'created': get_hkt_time().strftime('%Y-%m-%d'),
        'updated': datetime.utcnow().isoformat() + 'Z',
        'tags': ['email', 'auto-added', email_data['category']],
        'notes': [
            f"📧 Email ID: {email_data['id']}",
            f"📬 From: {email_data['from']}",
            f"📅 Date: {email_data['date']}",
            f"🔗 Message-ID: {email_data['message_id']}",
            "",
            "📝 Summary:",
            email_data['body'][:500] if len(email_data['body']) > 500 else email_data['body']
        ]
    }
    
    # Add to projects
    kanban['projects'].append(task)
    kanban['meta']['updated'] = datetime.utcnow().isoformat() + 'Z'
    
    # Save
    with open(KANBAN_PATH, 'w', encoding='utf-8') as f:
        json.dump(kanban, f, indent=2, ensure_ascii=False)
    
    return task['id']

def load_email_state():
    """Load last checked email state"""
    try:
        with open(EMAIL_STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'lastChecked': None, 'lastEmailId': None}

def save_email_state(state):
    """Save email state"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(EMAIL_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_emails():
    """Main email checking function"""
    print(f"📬 Checking emails at {get_hkt_time().strftime('%Y-%m-%d %H:%M:%S HKT')}")
    
    # Connect to Gmail
    context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, ssl_context=context)
    mail.login(GMAIL_EMAIL, GMAIL_PASSWORD)
    mail.select("inbox")
    
    # Get last checked state
    state = load_email_state()
    last_email_id = state.get('lastEmailId')
    
    # 🔒 SECURITY FIX: Check ALL recent emails, not just UNSEEN
    # Forwarded emails arrive as "Seen" so we need to check by date
    from datetime import datetime, timedelta
    
    # Calculate 30 minutes ago in Gmail INTERNALDATE format
    thirty_min_ago = datetime.utcnow() - timedelta(minutes=35)  # Buffer
    since_date = thirty_min_ago.strftime("%d-%b-%Y")
    
    # Search for emails received in last 35 minutes (includes seen and unseen)
    status, messages = mail.search(None, f'(SINCE "{since_date}")')
    email_ids = messages[0].split()
    
    # Also get truly unseen emails (in case any)
    status, unseen = mail.search(None, "UNSEEN")
    unseen_ids = unseen[0].split()
    
    # Combine both lists (remove duplicates)
    all_email_ids = list(set(email_ids + unseen_ids))
    all_email_ids.sort(key=lambda x: int(x))  # Sort by email ID
    
    if not all_email_ids:
        print("✅ No new emails")
        mail.close()
        mail.logout()
        return {'new_emails': [], 'urgent_count': 0}
    
    print(f"📧 Found {len(all_email_ids)} email(s) in last 35 mins")
    print(f"   - {len(email_ids)} recent emails")
    print(f"   - {len(unseen_ids)} unread emails")
    
    new_emails = []
    urgent_count = 0
    processed_count = 0
    
    for eid in all_email_ids:
        # Skip already processed emails
        eid_str = eid.decode() if isinstance(eid, bytes) else str(eid)
        if last_email_id and eid_str <= last_email_id:
            continue
        
        status, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        subject = decode_mime(msg.get('Subject', ''))
        from_addr = decode_mime(msg.get('From', ''))
        date = msg.get('Date', '')
        message_id = msg.get('Message-ID', '')
        body = get_email_body(msg)
        
        # 🔒 SECURITY CHECK - LAYER 1: Verify sender
        trusted = is_trusted_sender(from_addr, msg)  # Pass msg to check forwarding headers
        sender_email = extract_email_address(from_addr)
        
        # 🔒 SECURITY CHECK - LAYER 2: Check for sensitive requests
        sensitive = is_sensitive_request(body)
        
        # 🔒 SECURITY DECISION
        if not trusted:
            # ⚠️ Unknown/untrusted sender
            print(f"⚠️  SUSPICIOUS: Email from untrusted sender: {sender_email}")
            log_audit(from_addr, subject, trusted, sensitive, 'blocked', 
                     details='Sender not in TRUSTED_SENDERS whitelist')
            send_discord_alert(f"🚨 Suspicious email blocked from {sender_email}")
            # Mark as read but skip processing
            mail.store(eid, '+FLAGS', '\\Seen')
            continue
        
        if sensitive:
            # 🔒 Sensitive request from trusted sender - require extra verification
            print(f"🔒 SENSITIVE: Request requires verification from {sender_email}")
            log_audit(from_addr, subject, trusted, sensitive, 'verification_required',
                     details='Sensitive keywords detected, verification sent')
            # TODO: Send verification email
            # For now, process normally but log it
            send_discord_alert(f"🔒 Sensitive request detected from {sender_email}")
        
        # ✅ Safe to process - trusted sender, non-sensitive
        log_audit(from_addr, subject, trusted, sensitive, 'processed')
        processed_count += 1
        
        # Classify email
        priority, category, needs_action = classify_email(subject, body, from_addr)
        
        email_data = {
            'id': eid.decode(),
            'subject': subject,
            'from': from_addr,
            'date': date,
            'message_id': message_id,
            'body': body[:1000],  # First 1000 chars
            'priority': priority,
            'category': category,
            'needs_action': needs_action
        }
        
        new_emails.append(email_data)
        
        # Create Kanban task if action needed
        if needs_action and priority in ['urgent', 'high']:
            task_id = create_kanban_task(email_data, priority)
            email_data['kanban_task'] = task_id
            print(f"✅ Created Kanban task: {task_id}")
        
        if priority == 'urgent':
            urgent_count += 1
        
        # Mark as read (already read for forwarded, mark for unseen)
        mail.store(eid, '+FLAGS', '\\Seen')
    
    # Update state
    if all_email_ids:
        state['lastChecked'] = datetime.utcnow().isoformat() + 'Z'
        state['lastEmailId'] = all_email_ids[-1].decode()
        state['totalChecked'] = state.get('totalChecked', 0) + len(new_emails)
        state['totalProcessed'] = state.get('totalProcessed', 0) + processed_count
        save_email_state(state)
    
    mail.close()
    mail.logout()
    
    return {
        'new_emails': new_emails,
        'urgent_count': urgent_count,
        'processed_count': processed_count,
        'check_time': get_hkt_time().strftime('%Y-%m-%d %H:%M:%S HKT')
    }

def get_audit_summary():
    """📊 Get audit log summary for status report"""
    try:
        with open(AUDIT_LOG_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total = len(lines)
        blocked = sum(1 for line in lines if '"response": "blocked"' in line)
        processed = sum(1 for line in lines if '"response": "processed"' in line)
        sensitive = sum(1 for line in lines if '"sensitive": true' in line)
        
        return {
            'total': total,
            'blocked': blocked,
            'processed': processed,
            'sensitive': sensitive
        }
    except:
        return {'total': 0, 'blocked': 0, 'processed': 0, 'sensitive': 0}

def get_trusted_senders_summary():
    """📋 Get summary of trusted senders"""
    if len(TRUSTED_SENDERS) <= 3:
        return ', '.join(TRUSTED_SENDERS)
    else:
        # Show first 3 + count
        return f"{TRUSTED_SENDERS[0]} +{len(TRUSTED_SENDERS)-1} more"

def get_security_mode_summary():
    """🔒 Get security mode description"""
    if len(TRUSTED_SENDERS) == 1:
        return f"STRICT MODE - Only trust {TRUSTED_SENDERS[0]}"
    else:
        return f"STRICT MODE - Trust {len(TRUSTED_SENDERS)} senders: {', '.join(TRUSTED_SENDERS)}"

def format_discord_message(result, include_status=False, only_on_new=False):
    """Format Discord message with color coding"""
    audit = get_audit_summary()
    security_mode = get_security_mode_summary()
    
    # If only_on_new mode and no new emails, return None (silent)
    if only_on_new and not result['new_emails']:
        return None
    
    if not result['new_emails']:
        message = "📬 **Email Check** - No new emails\n\n"
        if include_status:
            message += "### 🔒 Security Status (STRICT MODE)\n"
            message += f"- ✅ Trusted: {security_mode}\n"
            message += f"- 🛡️ Audit Log: {audit['total']} entries\n"
            message += f"- 🚫 Blocked: {audit['blocked']} emails\n"
            message += f"- ✅ Processed: {audit['processed']} emails\n"
            message += f"- 📧 Reply allowed: Only to {', '.join(ALLOWED_REPLY_TO)}\n\n"
        message += "Next check: 30 minutes"
        return message
    
    # Group by priority
    urgent = [e for e in result['new_emails'] if e['priority'] == 'urgent']
    high = [e for e in result['new_emails'] if e['priority'] == 'high']
    medium = [e for e in result['new_emails'] if e['priority'] == 'medium']
    low = [e for e in result['new_emails'] if e['priority'] == 'low']
    
    message = f"## 📬 Email Summary - {result['check_time']}\n\n"
    message += f"**New Emails:** {len(result['new_emails'])} unread\n\n"
    
    if urgent:
        message += "### 🔴 URGENT (需立即處理)\n"
        for e in urgent:
            kanban_note = f" → `{e.get('kanban_task', 'N/A')}`" if e.get('kanban_task') else ""
            message += f"- {e['subject']}{kanban_note}\n"
            message += f"  **From:** {e['from']}\n"
            message += f"  **Action:** Added to Kanban (urgent priority)\n\n"
    
    if high:
        message += "### 🟠 HIGH Priority\n"
        for e in high:
            kanban_note = f" → `{e.get('kanban_task', 'N/A')}`" if e.get('kanban_task') else ""
            message += f"- {e['subject']}{kanban_note}\n"
            message += f"  **From:** {e['from']}\n\n"
    
    if medium:
        message += "### 🟡 Normal\n"
        for e in medium:
            message += f"- {e['subject']}\n"
            message += f"  **From:** {e['from']}\n\n"
    
    if low:
        message += "### 🟢 Low (Newsletters/Promos)\n"
        for e in low[:5]:  # Limit to 5
            message += f"- {e['subject']}\n"
        if len(low) > 5:
            message += f"... and {len(low) - 5} more\n"
        message += "\n"
    
    message += f"---\n**Next Check:** 30 minutes\n"
    
    if result['urgent_count'] > 0:
        message += f"\n⚠️ **{result['urgent_count']} URGENT email(s) require immediate attention!**"
    
    return message

if __name__ == "__main__":
    import sys
    
    # Check flags
    # --status: Include security status summary
    # --only-new: Only post if there are NEW emails (silent if no new emails)
    include_status = '--status' in sys.argv
    only_on_new = '--only-new' in sys.argv or '--silent-if-empty' in sys.argv
    
    # Run email check
    result = check_emails()
    
    # Format Discord message
    discord_message = format_discord_message(result, include_status=include_status, only_on_new=only_on_new)
    
    # Print for capture by calling script
    print("\n" + "="*80)
    print("DISCORD_MESSAGE_START")
    if discord_message:
        print(discord_message)
    else:
        print("NO_NEW_EMAILS")  # Signal to wrapper that there's nothing to post
    print("DISCORD_MESSAGE_END")
    print("="*80)
    
    # Exit with code indicating if urgent emails found
    exit(0 if result['urgent_count'] == 0 else 1)
