#!/usr/bin/env python3
"""
Discord Bot for Minimax M2.7 OpenClaw Agent
"""

import os
import json
import asyncio
import requests
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv('/home/node/.openclaw/workspace/agents/minimax-m2.7.env')

class MinimaxDiscordBot:
    """Discord bot for Minimax M2.7 agent"""
    
    def __init__(self):
        self.api_key = os.getenv('MINIMAX_M2.7_API_KEY')
        self.model = os.getenv('MINIMAX_M2.7_MODEL', 'abab6.5-chat')
        self.base_url = os.getenv('MINIMAX_M2.7_BASE_URL', 'https://api.minimaxi.com/v1')
        
        # Discord bot token (you need to set this in your .env file)
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        
        if not self.discord_token:
            print("⚠️ Warning: DISCORD_BOT_TOKEN not set. Bot will run in test mode.")
        
        # Initialize Discord bot
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        
        self.bot = commands.Bot(
            command_prefix='!m2 ',
            intents=intents,
            help_command=None
        )
        
        # Setup event handlers
        self.setup_handlers()
        
        # Track usage for quota monitoring
        self.message_count = 0
    
    def setup_handlers(self):
        """Setup Discord event handlers"""
        
        @self.bot.event
        async def on_ready():
            print(f'✅ {self.bot.user} has connected to Discord!')
            print(f'📋 Serving in {len(self.bot.guilds)} guild(s)')
            
            # Set bot status
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name="!m2 help"
                )
            )
        
        @self.bot.event
        async def on_message(message):
            # Don't respond to ourselves
            if message.author == self.bot.user:
                return
            
            # Check if bot is mentioned or command is used
            if self.bot.user in message.mentions or message.content.startswith('!m2'):
                await self.handle_message(message)
            
            # Process commands
            await self.bot.process_commands(message)
        
        # Add commands
        @self.bot.command(name='help')
        async def help_command(ctx):
            """Show help information"""
            help_text = """
**🤖 Minimax M2.7 OpenClaw Agent Commands:**

`!m2 help` - Show this help message
`!m2 ping` - Test if bot is responsive
`!m2 code <language> <task>` - Generate code
`!m2 ask <question>` - Ask any question
`!m2 cantonese <question>` - Ask in Cantonese
`!m2 quota` - Check API quota status
`!m2 test` - Run connection test

**Examples:**
`!m2 code python "sort list"`
`!m2 ask "Explain quantum computing"`
`!m2 cantonese "點樣學編程"`
`@Minimax-M2.7-Bot hello` - Mention the bot to chat

**Powered by:** Minimax M2.7 (abab6.5-chat)
            """
            await ctx.send(help_text)
        
        @self.bot.command(name='ping')
        async def ping(ctx):
            """Check bot latency"""
            latency = round(self.bot.latency * 1000, 2)
            await ctx.send(f'🏓 Pong! Latency: {latency}ms')
        
        @self.bot.command(name='code')
        async def generate_code(ctx, language: str, *, task: str):
            """Generate code in specified language"""
            await ctx.send(f"💻 Generating {language} code for: {task}")
            
            prompt = f"Write {language} code to {task}. Include comments and error handling."
            response = await self.call_minimax(prompt, temperature=0.3)
            
            # Format code response
            if len(response) > 1900:  # Discord message limit
                response = response[:1900] + "...\n\n(Response truncated due to length)"
            
            await ctx.send(f"```{language}\n{response}\n```")
        
        @self.bot.command(name='ask')
        async def ask_question(ctx, *, question: str):
            """Ask any question"""
            await ctx.send(f"🤔 Processing your question...")
            
            response = await self.call_minimax(question)
            await ctx.send(response)
        
        @self.bot.command(name='cantonese')
        async def ask_cantonese(ctx, *, question: str):
            """Ask question in Cantonese"""
            await ctx.send(f"🇭🇰 用廣東話回答...")
            
            prompt = f"用廣東話回答以下問題：{question}"
            response = await self.call_minimax(prompt)
            await ctx.send(response)
        
        @self.bot.command(name='quota')
        async def check_quota(ctx):
            """Check API quota status"""
            # This would call Minimax quota API if available
            # For now, show static info
            quota_info = """
**📊 Minimax M2.7 Quota Information:**

**Text Generation:**
• 4500 calls per 5-hour rolling window
• Current window: Unknown (API endpoint needed)
• Usage: Monitor via Minimax dashboard

**Media Generation (Daily):**
• Images: 120/day
• Video: 4 clips/day (2 fast + 2 standard)
• Music: 4 tracks/day
• TTS: 11,000 calls/day

**Reset Times:**
• Text: Rolling 5-hour window
• Media: Daily at 00:00 HKT

**Note:** Actual quota monitoring requires Minimax API support.
            """
            await ctx.send(quota_info)
        
        @self.bot.command(name='test')
        async def test_connection(ctx):
            """Test Minimax API connection"""
            await ctx.send("🔍 Testing Minimax M2.7 connection...")
            
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": "Say 'Minimax M2.7 is working with Discord!'"}
                        ],
                        "max_tokens": 50,
                        "temperature": 0.7
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    message = result['choices'][0]['message']['content']
                    await ctx.send(f"✅ Connection successful!\n{message}")
                else:
                    await ctx.send(f"❌ API Error: {response.status_code}")
                    
            except Exception as e:
                await ctx.send(f"❌ Connection failed: {str(e)}")
    
    async def handle_message(self, message):
        """Handle regular messages mentioning the bot"""
        # Extract clean message content (remove mention)
        content = message.content
        
        # Remove bot mention
        for mention in message.mentions:
            if mention == self.bot.user:
                content = content.replace(f'<@{mention.id}>', '').strip()
        
        # Remove command prefix if present
        if content.startswith('!m2'):
            content = content[3:].strip()
        
        if not content:
            content = "Hello! How can I help you today?"
        
        # Show typing indicator
        async with message.channel.typing():
            # Call Minimax API
            response = await self.call_minimax(content)
            
            # Track usage
            self.message_count += 1
            
            # Send response
            await message.reply(response)
    
    async def call_minimax(self, prompt, temperature=0.7):
        """Call Minimax M2.7 API"""
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1500,
                    "temperature": temperature
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ API Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"❌ Error calling Minimax: {str(e)}"
    
    def run(self):
        """Run the Discord bot"""
        if not self.discord_token:
            print("❌ Cannot start Discord bot: DISCORD_BOT_TOKEN not set")
            print("\n📝 To get a Discord bot token:")
            print("1. Go to https://discord.com/developers/applications")
            print("2. Create a new application")
            print("3. Go to Bot section and click 'Add Bot'")
            print("4. Copy the token and add to your .env file:")
            print("   DISCORD_BOT_TOKEN=your_token_here")
            print("5. Enable Message Content Intent in Bot settings")
            print("6. Invite bot to server with OAuth2 URL Generator")
            return False
        
        print("🚀 Starting Minimax M2.7 Discord Bot...")
        print(f"🤖 Model: {self.model}")
        print(f"🔗 API Base: {self.base_url}")
        print("📝 Use '!m2 help' for commands")
        
        try:
            self.bot.run(self.discord_token)
            return True
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            return False

def test_without_discord():
    """Test the Minimax integration without Discord"""
    print("🔧 Testing Minimax M2.7 integration (without Discord)...")
    
    bot = MinimaxDiscordBot()
    
    # Test API call
    print("\n📡 Testing API call...")
    test_prompt = "Write a Python function to check if a number is prime"
    
    # Use asyncio to run the async function
    async def test_async():
        response = await bot.call_minimax(test_prompt, temperature=0.3)
        print(f"✅ API Response:\n{response}")
    
    asyncio.run(test_async())
    
    print("\n🎯 Test completed!")
    print("\n📝 Next steps to use with Discord:")
    print("1. Get Discord bot token from https://discord.com/developers/applications")
    print("2. Add DISCORD_BOT_TOKEN to minimax-m2.7.env file")
    print("3. Run: python3 discord_minimax_bot.py")
    print("4. Use !m2 help in Discord for commands")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_without_discord()
    else:
        bot = MinimaxDiscordBot()
        bot.run()