# 🚀 Minimax M2.7 OpenClaw Agent Setup Guide

## 📋 What We've Created

### 1. **Agent Configuration**
- `minimax-m2.7-agent.json` - Agent definition and settings
- `minimax-m2.7.env` - Environment configuration (API keys)

### 2. **Test Scripts**
- `test_minimax_m2.7.py` - Comprehensive API testing
- `discord_minimax_bot.py` - Discord bot integration

### 3. **Documentation**
- This setup guide
- Discord testing instructions

---

## 🔧 Step 1: Test Minimax M2.7 Connection

### Run the test script:
```bash
cd /home/node/.openclaw/workspace/agents
python3 test_minimax_m2.7.py
```

### Expected Output:
```
🚀 Minimax M2.7 OpenClaw Agent Test Suite
============================================================

🔍 Testing Minimax M2.7 API connection...
✅ Connection successful!
🤖 Response: Minimax M2.7 is working!

💻 Testing programming capabilities...
✅ Programming test successful!
📝 Code generated: [Python code here]

🇭🇰 Testing Cantonese language support...
✅ Cantonese test successful!
🗣️ Response: [Cantonese response here]

📊 Checking quota information...
ℹ️ Quota monitoring would be implemented here
• Text quota: 4500 calls / 5 hours (rolling window)
• Media quotas reset daily at 00:00 HKT

🎯 Results: 4/4 tests passed
🏆 All tests passed! Minimax M2.7 agent is ready!
```

---

## 💬 Step 2: Test in Discord

### Option A: Quick Test (Without Full Discord Bot)
```bash
cd /home/node/.openclaw/workspace/agents
python3 discord_minimax_bot.py test
```

This will test the Minimax integration without running the Discord bot.

### Option B: Full Discord Bot Setup

#### 1. **Get Discord Bot Token:**
1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name it "Minimax M2.7 Agent"
3. Go to "Bot" section → Click "Add Bot"
4. Copy the **Token** (click "Reset Token" if needed)
5. Enable **Message Content Intent** under Privileged Gateway Intents

#### 2. **Update Environment File:**
Edit `minimax-m2.7.env`:
```bash
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

#### 3. **Invite Bot to Your Server:**
1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`, `applications.commands`
3. Select bot permissions: `Send Messages`, `Read Message History`, `Embed Links`
4. Copy the generated URL and open it in browser
5. Select your server to add the bot

#### 4. **Run the Discord Bot:**
```bash
cd /home/node/.openclaw/workspace/agents
python3 discord_minimax_bot.py
```

#### 5. **Test in Discord:**
Join your Discord server and use these commands:

```
!m2 help                    - Show all commands
!m2 ping                    - Test bot latency
!m2 code python "sort list" - Generate Python code
!m2 ask "Explain AI"        - Ask any question
!m2 cantonese "點樣學編程"   - Ask in Cantonese
!m2 quota                   - Check API quota
!m2 test                    - Test API connection

@Minimax-M2.7-Bot hello     - Mention the bot to chat
```

---

## 🎯 Step 3: Integration with OpenClaw

### 1. **Create OpenClaw Skill:**
```bash
mkdir -p /home/node/.openclaw/workspace/skills/minimax-m2.7
```

Create `/home/node/.openclaw/workspace/skills/minimax-m2.7/SKILL.md`:
```markdown
# Minimax M2.7 Skill

## Description
Integration with Minimax M2.7 model for advanced text generation and coding tasks.

## Commands
- `minimax ask <question>` - Ask Minimax M2.7 a question
- `minimax code <language> <task>` - Generate code
- `minimax cantonese <question>` - Ask in Cantonese

## Configuration
Requires MINIMAX_M2.7_API_KEY in environment.
```

### 2. **Create Skill Script:**
Create `/home/node/.openclaw/workspace/skills/minimax-m2.7/minimax_skill.py`:
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv('/home/node/.openclaw/workspace/agents/minimax-m2.7.env')

def ask_minimax(question, temperature=0.7):
    """Ask Minimax M2.7 a question"""
    api_key = os.getenv('MINIMAX_M2.7_API_KEY')
    
    response = requests.post(
        "https://api.minimaxi.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "abab6.5-chat",
            "messages": [{"role": "user", "content": question}],
            "temperature": temperature
        }
    )
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}"
```

### 3. **Test in OpenClaw:**
```bash
# From OpenClaw chat
minimax ask "What is OpenClaw?"
minimax code python "web scraper"
minimax cantonese "介紹下 OpenClaw"
```

---

## 📊 Step 4: Quota Monitoring

### Create Quota Monitor:
```python
# File: quota_monitor.py
import time
from datetime import datetime, timedelta

class MinimaxQuotaMonitor:
    def __init__(self):
        self.calls = []
        self.quota_limit = 4500
        self.window_hours = 5
        
    def log_call(self):
        """Log an API call"""
        self.calls.append(datetime.now())
        self.clean_old_calls()
        
    def clean_old_calls(self):
        """Remove calls older than window"""
        cutoff = datetime.now() - timedelta(hours=self.window_hours)
        self.calls = [call for call in self.calls if call > cutoff]
        
    def get_usage(self):
        """Get current usage"""
        self.clean_old_calls()
        return len(self.calls)
    
    def get_remaining(self):
        """Get remaining calls"""
        return self.quota_limit - self.get_usage()
    
    def get_percentage(self):
        """Get usage percentage"""
        return (self.get_usage() / self.quota_limit) * 100
    
    def should_alert(self, threshold=80):
        """Check if should alert"""
        return self.get_percentage() >= threshold
```

### Usage:
```python
monitor = MinimaxQuotaMonitor()
monitor.log_call()  # Call this after each API request
print(f"Usage: {monitor.get_usage()}/{monitor.quota_limit}")
print(f"Remaining: {monitor.get_remaining()}")
```

---

## 🚨 Troubleshooting

### Common Issues:

#### 1. **API Key Not Working:**
```
❌ Connection failed: 401 Unauthorized
```
**Solution:** Check your `MINIMAX_M2.7_API_KEY` in the `.env` file.

#### 2. **Discord Bot Not Responding:**
```
❌ Cannot start Discord bot: DISCORD_BOT_TOKEN not set
```
**Solution:** Get a Discord bot token and add it to `.env` file.

#### 3. **Rate Limiting:**
```
❌ API Error: 429 Too Many Requests
```
**Solution:** Wait and retry. Monitor your quota (4500 calls/5 hours).

#### 4. **Model Not Found:**
```
❌ API Error: 404 Model not found
```
**Solution:** Check `MINIMAX_M2.7_MODEL` is set to `abab6.5-chat`.

---

## 🎯 Advanced Features

### 1. **Web Interface:**
Create a simple Flask web interface:
```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    # Call Minimax API
    return jsonify({"answer": "Minimax response here"})
```

### 2. **Slack Integration:**
Similar to Discord bot but for Slack workspace.

### 3. **Telegram Bot:**
Use python-telegram-bot library for Telegram integration.

### 4. **Scheduled Tasks:**
Use cron jobs or schedule library for automated tasks.

---

## 📈 Performance Tips

### 1. **Optimize Token Usage:**
- Set appropriate `max_tokens` for each request
- Use streaming for long responses
- Cache frequent queries

### 2. **Error Handling:**
- Implement retry logic with exponential backoff
- Log all API calls for debugging
- Set up alerts for quota exhaustion

### 3. **Cost Management:**
- Monitor usage daily
- Set budget alerts
- Use cheaper models for simple tasks

---

## 🔗 Resources

### Official Documentation:
- [Minimax API Docs](https://api.minimaxi.com/document)
- [Minimax Platform](https://platform.minimaxi.com)

### OpenClaw Integration:
- [OpenClaw Skills Guide](https://docs.openclaw.ai/skills)
- [OpenClaw Discord](https://discord.com/invite/clawd)

### Discord Bot:
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers)

---

## 🏆 Success Metrics

### Track These Metrics:
1. **API Success Rate:** Target > 99%
2. **Response Time:** Target < 3 seconds
3. **Quota Utilization:** Stay below 80%
4. **User Satisfaction:** Monitor Discord engagement

### Regular Maintenance:
- Weekly: Check API key validity
- Monthly: Review quota usage patterns
- Quarterly: Update to latest Minimax models

---

**🎉 Your Minimax M2.7 OpenClaw Agent is now ready!**

Start with the test script, then move to Discord integration, and finally integrate with OpenClaw for seamless AI assistance! 🚀