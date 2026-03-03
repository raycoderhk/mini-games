"""
《啓示路：樂土之門》Discord Bot - Simple Version
"""

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import json
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Database
def init_db():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id TEXT PRIMARY KEY,
            current_chapter INTEGER DEFAULT 1,
            current_scene TEXT DEFAULT 'scene_0',
            love_score INTEGER DEFAULT 0,
            truth_score INTEGER DEFAULT 0,
            afterland_score INTEGER DEFAULT 0,
            choices_made TEXT DEFAULT '[]',
            last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_progress(user_id, chapter, scene, love, truth, afterland, choices):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO players 
        (user_id, current_chapter, current_scene, love_score, truth_score, 
         afterland_score, choices_made, last_played)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, chapter, scene, love, truth, afterland, json.dumps(choices), datetime.now()))
    conn.commit()
    conn.close()

def get_progress(user_id):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'user_id': row[0], 'current_chapter': row[1], 'current_scene': row[2],
            'love_score': row[3], 'truth_score': row[4], 'afterland_score': row[5],
            'choices_made': json.loads(row[6])
        }
    return None

def load_chapter(chapter_num):
    script_path = f'scripts/chapter_{chapter_num}.json'
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

class GameView(View):
    def __init__(self, choices, user_id, chapter_data, scores):
        super().__init__(timeout=600)
        self.choices = choices
        self.user_id = user_id
        self.chapter_data = chapter_data
        self.scores = scores
        
        for i, choice in enumerate(choices):
            style = discord.ButtonStyle.primary
            if choice['emoji'] in ['❤️', '✨', '😂']:
                style = discord.ButtonStyle.success
            elif choice['emoji'] in ['🔍', '🤔']:
                style = discord.ButtonStyle.secondary
            
            btn = Button(label=choice['text'][:45], style=style, emoji=choice['emoji'], custom_id=f"choice_{i}")
            btn.callback = self.make_callback(choice)
            self.add_item(btn)
    
    def make_callback(self, choice):
        async def callback(interaction: discord.Interaction):
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message("❌ 唔係你嘅遊戲！", ephemeral=True)
                return
            
            self.scores['love'] += choice['effects']['love']
            self.scores['truth'] += choice['effects']['truth']
            self.scores['afterland'] += choice['effects']['afterland']
            
            progress = get_progress(self.user_id)
            choices_list = progress['choices_made'] if progress else []
            choices_list.append(choice['text'])
            
            save_progress(self.user_id, self.chapter_data['chapter'], choice['next'],
                         self.scores['love'], self.scores['truth'], self.scores['afterland'], choices_list)
            
            next_scene = None
            for scene in self.chapter_data['scenes']:
                if scene['id'] == choice['next']:
                    next_scene = scene
                    break
            
            if next_scene:
                text = next_scene['text']
                embed = discord.Embed(title="🌊 啓示路：樂土之門", description=text, color=discord.Color.purple())
                
                if next_scene['choices']:
                    new_view = GameView(next_scene['choices'], self.user_id, self.chapter_data, self.scores)
                    await interaction.response.edit_message(embed=embed, view=new_view)
                else:
                    await interaction.response.edit_message(embed=embed, view=None)
        
        return callback

@bot.tree.command(name="revelation", description="啓示路遊戲")
async def revelation(interaction: discord.Interaction, action: str):
    user_id = str(interaction.user.id)
    
    if action == "start":
        chapter_data = load_chapter(1)
        if not chapter_data:
            await interaction.response.send_message("❌ 劇本載入失敗", ephemeral=True)
            return
        
        save_progress(user_id, 1, 'scene_0', 0, 0, 0, [])
        scene = chapter_data['scenes'][0]
        scores = {'love': 0, 'truth': 0, 'afterland': 0}
        
        embed = discord.Embed(title="🌊 啓示路：樂土之門", description=scene['text'], color=discord.Color.purple())
        embed.set_footer(text="🔘 點擊下方按鈕")
        
        view = GameView(scene['choices'], user_id, chapter_data, scores)
        await interaction.response.send_message(embed=embed, view=view)
    
    elif action == "status":
        progress = get_progress(user_id)
        if not progress:
            await interaction.response.send_message("❌ 未找到進度", ephemeral=True)
            return
        
        embed = discord.Embed(title="📊 遊戲狀態", color=discord.Color.purple())
        embed.add_field(name="章節", value=f"第 {progress['current_chapter']} 章")
        embed.add_field(name="❤️ 愛情", value=str(progress['love_score']))
        embed.add_field(name="🔍 真相", value=str(progress['truth_score']))
        embed.add_field(name="🌐 樂土", value=str(progress['afterland_score']))
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="test", description="測試按鈕")
async def test(interaction: discord.Interaction):
    class TestView(View):
        def __init__(self):
            super().__init__(timeout=600)
        
        async def callback(interaction: discord.Interaction):
            await interaction.response.send_message("✅ 按鈕工作正常！", ephemeral=True)
    
    btn = Button(label="測試按鈕", style=discord.ButtonStyle.success, emoji="✅", custom_id="test_btn")
    btn.callback = callback
    
    view = View(timeout=600)
    view.add_item(btn)
    
    embed = discord.Embed(title="🔧 按鈕測試", description="如果見到下方按鈕，請撳佢！", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print(f'{bot.user} 已登入！')
    init_db()
    try:
        synced = await bot.tree.sync()
        print(f"已同步 {len(synced)} 個命令")
    except Exception as e:
        print(f"同步失敗：{e}")

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
