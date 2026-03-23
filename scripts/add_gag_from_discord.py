#!/usr/bin/env python3
"""
Add Gag from Discord Message
呢個腳本用於 OpenClaw 環境，通過 message tool 讀取 Discord 訊息並提交到 GitHub

Usage:
    python3 add_gag_from_discord.py --channel-id 1485598655430918165 --limit 10
"""

import json
import os
import sys
import requests
import re
from datetime import datetime, timedelta

# Config
GITHUB_OWNER = 'raycoderhk'
GITHUB_REPO = 'mini-games'
GITHUB_PATH = 'gag/gags.json'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

# Discord channel to monitor
GAG_CHANNEL_ID = '1485598655430918165'  # #gag channel

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
    
    Supported formats:
    1. Labeled:
       題目：XXXX？
       答案：XXXX
       出品人：@XXX
    
    2. Simple (by lines):
       XXXX？
       XXXX
       @XXX
    
    3. Inline:
       "題目？答案 @出品人"
    """
    lines = content.strip().split('\n')
    
    question = None
    answer = None
    author = None
    
    # Try labeled format first
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for labels (case insensitive)
        if re.match(r'題目 [:：]', line, re.IGNORECASE):
            question = re.split(r'題目 [:：]', line, maxsplit=1)[1].strip()
        elif re.match(r'答案 [:：]', line, re.IGNORECASE):
            answer = re.split(r'答案 [:：]', line, maxsplit=1)[1].strip()
        elif re.match(r'出品人 [:：]', line, re.IGNORECASE):
            author = re.split(r'出品人 [:：]', line, maxsplit=1)[1].strip()
        elif re.match(r'author [:：]', line, re.IGNORECASE):
            author = re.split(r'author [:：]', line, maxsplit=1)[1].strip()
        elif line.startswith('@') and not author:
            # Extract @mention
            mentions = re.findall(r'@\w+', line)
            if mentions:
                author = mentions[0]
    
    # If no labels, try to parse by line position
    if not question and len(lines) >= 1:
        # First non-empty line that's not an @mention
        for line in lines:
            line = line.strip()
            if line and not line.startswith('@'):
                question = line
                break
    
    if not answer and len(lines) >= 2:
        # Second non-empty line that's not an @mention
        count = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('@'):
                count += 1
                if count == 2:
                    answer = line
                    break
    
    if not author:
        # Try to find @mention anywhere
        mentions = re.findall(r'@\w+', content)
        if mentions:
            author = mentions[-1]  # Use last @mention as author
    
    return question, answer, author

def is_gag_message(content):
    """Check if message looks like a gag submission"""
    content_lower = content.lower()
    
    # Check for gag indicators
    indicators = [
        '題目', '答案', '出品人',
        'question', 'answer', 'author',
        '@'  # @mention for author
    ]
    
    # Count how many indicators are present
    count = sum(1 for ind in indicators if ind in content_lower)
    
    # Also check if it has multiple lines (likely Q&A format)
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    # Valid if: has 2+ indicators OR has 2+ lines with @mention
    return count >= 2 or (len(lines) >= 2 and '@' in content)

def add_gag(question, answer, author, sender_name='Unknown'):
    """Add new gag to GitHub"""
    if not question or not answer:
        print(f"❌ Missing question or answer")
        return False
    
    if not author:
        author = f'@{sender_name}'
    
    gags = get_github_file()
    
    new_gag = {
        'id': int(datetime.now().timestamp() * 1000),
        'question': question.strip(),
        'answer': answer.strip(),
        'author': author.strip(),
        'date': datetime.now().isoformat()
    }
    
    gags.insert(0, new_gag)
    
    message = f"🥚 Add new gag from Discord by {author}: {question[:30]}..."
    return commit_to_github(gags, message)

def process_messages(messages):
    """Process list of Discord messages"""
    processed = []
    
    for msg in messages:
        content = msg.get('content', '')
        sender = msg.get('author', {}).get('username', 'Unknown')
        message_id = msg.get('id', '')
        
        if not is_gag_message(content):
            print(f"⏭️  Skipping (not a gag): {content[:50]}...")
            continue
        
        question, answer, author = parse_gag_from_message(content)
        
        if not question or not answer:
            print(f"️  Skipping (incomplete): {content[:50]}...")
            continue
        
        # Use provided author or fallback to sender
        if not author or author == '@Unknown':
            author = f'@{sender}'
        
        print(f"\n📝 Found gag from {sender}:")
        print(f"   Q: {question}")
        print(f"   A: {answer}")
        print(f"   By: {author}")
        
        if add_gag(question, answer, author, sender):
            processed.append(message_id)
            print(f"   ✅ Added!")
        else:
            print(f"   ❌ Failed to add")
    
    return processed

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Add gags from Discord messages')
    parser.add_argument('--messages', type=str, help='JSON string of messages to process')
    parser.add_argument('--test', action='store_true', help='Test mode with sample message')
    
    args = parser.parse_args()
    
    if args.test:
        # Test mode
        test_messages = [
            {
                'id': 'test1',
                'content': '題目：點解路易十六食自助餐唔使俾錢？\n答案：因為自助餐係按人頭收費\n出品人：@MW',
                'author': {'username': 'raymond'}
            },
            {
                'id': 'test2',
                'content': '孔子和耶穌邊個厲害啲？\n耶穌，因為耶穌手上有兩個孔子，腳上有一個孔子，背後還有一個莊子。\n@MW',
                'author': {'username': 'raymond'}
            }
        ]
        
        print("🧪 Test mode - processing sample messages\n")
        processed = process_messages(test_messages)
        print(f"\n✅ Processed {len(processed)} gags")
        return
    
    if not args.messages:
        print("❌ No messages provided. Use --messages or --test")
        print("\nUsage:")
        print("  python3 add_gag_from_discord.py --test")
        print("  python3 add_gag_from_discord.py --messages '[{\"id\":\"...\",\"content\":\"...\",\"author\":{\"username\":\"...\"}}]'")
        sys.exit(1)
    
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    try:
        messages = json.loads(args.messages)
        if not isinstance(messages, list):
            messages = [messages]
        
        print(f"📬 Processing {len(messages)} messages...\n")
        processed = process_messages(messages)
        
        print(f"\n✅ Done! Processed {len(processed)} gags")
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
