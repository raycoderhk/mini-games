#!/usr/bin/env python3
"""
爛 Gag Discord Monitor
監察 #gag channel 嘅新訊息，自動解析並提交到 GitHub
"""

import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# Config
GITHUB_OWNER = 'raycoderhk'
GITHUB_REPO = 'mini-games'
GITHUB_PATH = 'gag/gags.json'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

# State file
STATE_FILE = Path(__file__).parent / '.discord_monitor_state.json'

def load_state():
    """Load last processed message ID"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'last_message_id': None, 'processed_messages': []}

def save_state(state):
    """Save state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_github_file():
    """Get current gags.json from GitHub"""
    url = f'https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/main/{GITHUB_PATH}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def get_file_sha():
    """Get file SHA for commit"""
    url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_PATH}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('sha')
    return None

def commit_to_github(gags, message):
    """Commit updated gags to GitHub"""
    url = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_PATH}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    sha = get_file_sha()
    if not sha:
        print("❌ Cannot get file SHA")
        return False
    
    data = {
        'message': message,
        'content': json.dumps(gags, indent=2, ensure_ascii=False),
        'sha': sha
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"✅ Committed: {message}")
        return True
    else:
        print(f"❌ Commit failed: {response.status_code}")
        print(response.text)
        return False

def parse_gag_from_message(content):
    """
    Parse gag from Discord message
    Expected format:
    題目：XXXX？
    答案：XXXX
    出品人：@XXX
    
    Or simpler:
    XXXX？
    XXXX
    @XXX
    """
    lines = content.strip().split('\n')
    
    question = None
    answer = None
    author = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.lower().startswith('題目：') or line.lower().startswith('question:'):
            question = line.split(':', 1)[1].strip()
        elif line.lower().startswith('答案：') or line.lower().startswith('answer:'):
            answer = line.split(':', 1)[1].strip()
        elif line.lower().startswith('出品人：') or line.lower().startswith('author:'):
            author = line.split(':', 1)[1].strip()
        elif line.startswith('@'):
            author = line.strip()
    
    # If no explicit labels, try to parse by position
    if not question and len(lines) >= 2:
        question = lines[0].strip()
        answer = lines[1].strip()
        if len(lines) >= 3:
            author = lines[2].strip()
    
    return question, answer, author

def add_gag(question, answer, author):
    """Add new gag to GitHub"""
    if not question or not answer:
        print("❌ Missing question or answer")
        return False
    
    if not author:
        author = '@Unknown'
    
    gags = get_github_file()
    
    new_gag = {
        'id': datetime.now().timestamp(),
        'question': question,
        'answer': answer,
        'author': author,
        'date': datetime.now().isoformat()
    }
    
    gags.insert(0, new_gag)
    
    message = f"🥚 Add new gag from Discord by {author}: {question[:30]}..."
    return commit_to_github(gags, message)

def check_discord_messages():
    """
    Check Discord messages via OpenClaw message API
    This is a placeholder - actual implementation depends on OpenClaw's Discord integration
    """
    print("📬 Checking Discord messages...")
    
    # Note: This requires OpenClaw's Discord integration
    # For now, this is a placeholder that shows how it would work
    
    state = load_state()
    last_message_id = state.get('last_message_id')
    
    # In real implementation, you would:
    # 1. Call OpenClaw message API to get recent messages from #gag channel
    # 2. Filter messages from users (not bots)
    # 3. Parse each message for gag content
    # 4. Add valid gags to GitHub
    
    print("ℹ️  Discord integration requires OpenClaw message API")
    print("ℹ️  For now, use Admin Panel or send gags to the channel for manual processing")
    
    return 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test mode - parse a sample message
        test_content = """題目：點解路易十六食自助餐唔使俾錢？
答案：因為自助餐係按人頭收費
出品人：@MW"""
        
        q, a, auth = parse_gag_from_message(test_content)
        print(f"Question: {q}")
        print(f"Answer: {a}")
        print(f"Author: {auth}")
        return
    
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    check_discord_messages()

if __name__ == '__main__':
    main()
