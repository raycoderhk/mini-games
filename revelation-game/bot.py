"""
《啓示路：樂土之門》Discord Bot
基於 Discord.py 的互動文字冒險遊戲
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

# 載入環境變量
load_dotenv()

# 初始化 Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# 數據庫初始化
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
            endings_unlocked TEXT DEFAULT '[]',
            last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 儲存玩家進度
def save_progress(user_id, chapter, scene, love, truth, afterland, choices):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO players 
        (user_id, current_chapter, current_scene, love_score, truth_score, 
         afterland_score, choices_made, last_played)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, chapter, scene, love, truth, afterland, 
          json.dumps(choices), datetime.now()))
    conn.commit()
    conn.close()

# 讀取玩家進度
def get_progress(user_id):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'user_id': row[0],
            'current_chapter': row[1],
            'current_scene': row[2],
            'love_score': row[3],
            'truth_score': row[4],
            'afterland_score': row[5],
            'choices_made': json.loads(row[6]),
            'last_played': row[8]
        }
    return None

# 載入劇本
def load_chapter(chapter_num):
    script_path = f'scripts/chapter_{chapter_num}.json'
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# 生成場景 Embed
def create_scene_embed(scene_data, scores):
    text = scene_data['text'].format(
        love=scores['love'],
        truth=scores['truth'],
        afterland=scores['afterland']
    )
    
    embed = discord.Embed(
        title="🌊 啓示路：樂土之門",
        description=text,
        color=discord.Color.purple()
    )
    embed.set_footer(text="🔘 點擊下方按鈕做選擇")
    return embed

# 生成選擇視圖
class ChoiceView(View):
    def __init__(self, choices, user_id, chapter_data, current_scores, message=None):
        super().__init__(timeout=None)  # 無超時 (永久有效)
        self.choices = choices
        self.user_id = user_id
        self.chapter_data = chapter_data
        self.scores = current_scores.copy()
        self.message = message
        
        # 添加按鈕
        for i, choice in enumerate(choices):
            # 根據選擇類型使用不同風格
            if choice['emoji'] in ['❤️', '😂', '✨']:
                style = discord.ButtonStyle.success
            elif choice['emoji'] in ['🔍', '🤔', '😐']:
                style = discord.ButtonStyle.secondary
            elif choice['emoji'] in ['🌐', '😤']:
                style = discord.ButtonStyle.primary
            else:
                style = discord.ButtonStyle.primary
            
            button = Button(
                label=choice['text'][:50],
                style=style,
                emoji=choice['emoji'],
                custom_id=f"revelation_choice_{user_id}_{i}"
            )
            button.callback = self.make_callback(choice, i)
            self.add_item(button)
    
    def make_callback(self, choice, index):
        async def callback(interaction: discord.Interaction):
            # 驗證用戶
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message(
                    "❌ 呢個唔係你嘅遊戲！",
                    ephemeral=True
                )
                return
            
            # 更新數值
            self.scores['love'] += choice['effects']['love']
            self.scores['truth'] += choice['effects']['truth']
            self.scores['afterland'] += choice['effects']['afterland']
            
            # 儲存進度
            choices_made = get_progress(self.user_id)
            if choices_made:
                choices_list = choices_made.get('choices_made', [])
            else:
                choices_list = []
            choices_list.append(choice['text'])
            
            save_progress(
                self.user_id,
                self.chapter_data['chapter'],
                choice['next'],
                self.scores['love'],
                self.scores['truth'],
                self.scores['afterland'],
                choices_list
            )
            
            # 查找下一場景
            next_scene = None
            for scene in self.chapter_data['scenes']:
                if scene['id'] == choice['next']:
                    next_scene = scene
                    break
            
            if next_scene:
                # 創建新場景的 Embed
                embed = create_scene_embed(next_scene, self.scores)
                
                # 發送新場景（帶對話和按鈕）
                if next_scene['choices']:
                    new_view = ChoiceView(
                        next_scene['choices'],
                        self.user_id,
                        self.chapter_data,
                        self.scores
                    )
                    # 直接發送新消息
                    await interaction.response.send_message(embed=embed, view=new_view)
                else:
                    await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("❌ 場景錯誤", ephemeral=True)
        
        return callback
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        try:
            if self.message:
                await self.message.edit(view=self)
        except:
            pass

# Slash Commands
@bot.tree.command(name="revelation", description="啓示路遊戲命令")
async def revelation(interaction: discord.Interaction, action: str):
    user_id = str(interaction.user.id)
    
    if action == "start":
        # 開始新遊戲
        chapter_data = load_chapter(1)
        if not chapter_data:
            await interaction.response.send_message("❌ 劇本載入失敗", ephemeral=True)
            return
        
        # 初始化玩家數據
        save_progress(user_id, 1, 'scene_0', 0, 0, 0, [])
        
        # 發送開場
        scene = chapter_data['scenes'][0]
        scores = {'love': 0, 'truth': 0, 'afterland': 0}
        embed = create_scene_embed(scene, scores)
        
        view = ChoiceView(scene['choices'], user_id, chapter_data, scores)
        response = await interaction.response.send_message(embed=embed, view=view)
        
        # 儲存 message 用於超時處理
        if hasattr(response, 'message'):
            view.message = response.message
    
    elif action == "continue":
        # 繼續遊戲
        progress = get_progress(user_id)
        if not progress:
            await interaction.response.send_message(
                "❌ 未找到遊戲進度，請先輸入 /revelation start",
                ephemeral=True
            )
            return
        
        chapter_data = load_chapter(progress['current_chapter'])
        if not chapter_data:
            await interaction.response.send_message("❌ 劇本載入失敗", ephemeral=True)
            return
        
        # 查找當前場景
        current_scene = None
        for scene in chapter_data['scenes']:
            if scene['id'] == progress['current_scene']:
                current_scene = scene
                break
        
        if not current_scene:
            current_scene = chapter_data['scenes'][0]
        
        scores = {
            'love': progress['love_score'],
            'truth': progress['truth_score'],
            'afterland': progress['afterland_score']
        }
        
        embed = create_scene_embed(current_scene, scores)
        
        if current_scene['choices']:
            view = ChoiceView(current_scene['choices'], user_id, chapter_data, scores)
            response = await interaction.response.send_message(embed=embed, view=view)
            if hasattr(response, 'message'):
                view.message = response.message
        else:
            await interaction.response.send_message(embed=embed)
    
    elif action == "status":
        # 查看狀態
        progress = get_progress(user_id)
        if not progress:
            await interaction.response.send_message(
                "❌ 未找到遊戲進度",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="📊 遊戲狀態",
            color=discord.Color.purple()
        )
        embed.add_field(name="當前章節", value=f"第 {progress['current_chapter']} 章")
        embed.add_field(name="❤️ 愛情值", value=str(progress['love_score']))
        embed.add_field(name="🔍 真相值", value=str(progress['truth_score']))
        embed.add_field(name="🌐 樂土值", value=str(progress['afterland_score']))
        embed.add_field(name="已做選擇", value=str(len(progress['choices_made'])))
        embed.set_footer(text=f"最後遊玩：{progress['last_played']}")
        
        await interaction.response.send_message(embed=embed)
    
    elif action == "reset":
        # 重置進度
        conn = sqlite3.connect('players.db')
        c = conn.cursor()
        c.execute('DELETE FROM players WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        await interaction.response.send_message(
            "✅ 進度已重置，輸入 /revelation start 重新開始",
            ephemeral=True
        )

@bot.tree.command(name="help", description="顯示幫助信息")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎮 《啓示路：樂土之門》幫助",
        description="基於鄧紫棋科幻小說《啓示路》的互動文字冒險遊戲",
        color=discord.Color.purple()
    )
    embed.add_field(
        name="📜 遊戲命令",
        value="""
        `/revelation start` - 開始新遊戲
        `/revelation continue` - 繼續遊戲
        `/revelation status` - 查看角色狀態
        `/revelation reset` - 重置進度
        """,
        inline=False
    )
    embed.add_field(
        name="💡 遊戲提示",
        value="""
        - 你的選擇會影響三個數值
        - 不同數值組合會解鎖不同結局
        - 共有 6 個結局等待解鎖
        """,
        inline=False
    )
    embed.set_footer(text="祝你遊戲愉快！")
    
    await interaction.response.send_message(embed=embed)

# Bot 事件
@bot.event
async def on_ready():
    print(f'{bot.user} 已登入！')
    init_db()
    try:
        synced = await bot.tree.sync()
        print(f"已同步 {len(synced)} 個命令")
    except Exception as e:
        print(f"同步失敗：{e}")

# 運行 Bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("錯誤：請設置 DISCORD_TOKEN 環境變量")
        exit(1)
    bot.run(TOKEN)
