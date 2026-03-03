# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Gmail Configuration

**Account:** [Gmail address for OpenClaw]
**App Password:** Stored in `pass` (gmail/openclaw) or keyring
**IMAP:** imap.gmail.com:993 (TLS)
**SMTP:** smtp.gmail.com:587 (STARTTLS)

### Setup Checklist
- [ ] Create Gmail account
- [ ] Enable 2FA on Google Account
- [ ] Generate App Password: https://myaccount.google.com/apppasswords
- [ ] Enable IMAP in Gmail settings
- [ ] Run setup script: `skills/gmail/scripts/setup-gmail.sh`
- [ ] Configure email forwarding from main email

### Config Location
`~/.config/himalaya/config.toml`
