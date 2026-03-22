#!/usr/bin/env python3
"""
YouTube Monitor - Discord Integration
Sends new video notifications to Discord using Discord Bot API
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
NEW_VIDEOS_FILE = MEMORY_DIR / "youtube-new-videos.json"
SENT_VIDEOS_FILE = MEMORY_DIR / "youtube-sent.json"

# Discord Configuration
DISCORD_BOT_TOKEN = "${DISCORD_BOT_TOKEN}"  # Set via environment variable
DISCORD_CHANNEL_ID = "${DISCORD_CHANNEL_ID}"  # Set via environment variable

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def send_discord_message(channel_id, message):
    """Send message to Discord channel using Bot API"""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {"content": message, "tts": False}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Sent to Discord: {channel_id}")
            return True
        else:
            print(f"❌ Discord API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Failed to send: {e}")
        return False
    
def clean_description(description):
    """Clean description: remove URLs, extract key info for summary"""
    import re
    
    if not description or description == '無描述':
        return '無描述'
    
    # Remove all URLs (http, https, youtu.be, youtube.com)
    url_pattern = r'https?://[^\s\n]+'
    clean_text = re.sub(url_pattern, '', description)
    
    # Remove common YouTube boilerplate
    boilerplate_patterns = [
        r'🔔.*?subscribe',
        r'👉.*?follow',
        r'💬.*?comment',
        r'👍.*?like',
        r'📢.*?share',
        r'Follow.*?social',
        r'Check out.*?channel',
        r'🔗.*?link',
    ]
    
    for pattern in boilerplate_patterns:
        clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)
    
    # Clean up whitespace
    clean_text = '\n'.join([line.strip() for line in clean_text.split('\n') if line.strip()])
    
    # Extract first 2-3 meaningful lines as summary
    lines = [l for l in clean_text.split('\n') if len(l) > 20 and not l.startswith('#')]
    summary_lines = lines[:3]
    
    if summary_lines:
        summary = '\n'.join(summary_lines)
        if len(summary) > 400:
            summary = summary[:397] + '...'
        return summary
    
    return clean_text[:400] + '...' if len(clean_text) > 400 else clean_text

def main():
    """Check for new videos and send notifications"""
    print(f"[{datetime.now().isoformat()}] Checking for new videos to notify...")
    
    # Load new videos from check_videos.py
    new_videos_data = load_json(NEW_VIDEOS_FILE)
    
    if not new_videos_data or 'videos' not in new_videos_data:
        print("No new videos to notify")
        return
    
    # Load sent videos (to avoid duplicates)
    sent_videos = load_json(SENT_VIDEOS_FILE, {'video_ids': []})
    sent_ids = set(sent_videos.get('video_ids', []))
    
    videos_to_notify = []
    
    for item in new_videos_data.get('videos', []):
        video = item.get('video', {})
        video_id = video.get('video_id')
        
        # Skip if already sent
        if video_id in sent_ids:
            continue
        
        videos_to_notify.append(item)
        sent_ids.add(video_id)
    
    if not videos_to_notify:
        print("All videos already notified")
        return
    
    # Send notifications
    print(f"Sending {len(videos_to_notify)} notification(s)...")
    
    for item in videos_to_notify:
        video = item['video']
        channel_name = item['channel_name']
        
        # Format message
        published = video.get('published', '')
        try:
            dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
            hkt_time = dt.strftime('%Y-%m-%d %H:%M HKT')
        except:
            hkt_time = published
        
        # Clean and summarize description (remove all links except main video)
        summary = clean_description(video.get('description', ''))
        
        message = f"""## 🎬 YouTube 新片通知

**頻道:** {channel_name}
**標題:** {video['title']}
**發布:** {hkt_time}

**總結:**
{summary}

📺 觀看視頻：{video['url']}"""
        
        # Send to Discord
        send_discord_message(DISCORD_CHANNEL_ID, message)
    
    # Save sent video IDs
    save_json(SENT_VIDEOS_FILE, {
        'lastUpdate': datetime.now(timezone.utc).isoformat(),
        'video_ids': list(sent_ids)
    })
    
    # Clear processed videos
    save_json(NEW_VIDEOS_FILE, {'processed': True})
    
    print(f"✅ Sent {len(videos_to_notify)} notification(s)")

if __name__ == '__main__':
    main()
