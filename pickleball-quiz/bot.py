import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import json, sqlite3, os, traceback, random

load_dotenv()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

def init_db():
    conn = sqlite3.connect('pickleball_quiz.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores (
        user_id TEXT PRIMARY KEY, 
        total_questions INTEGER DEFAULT 0,
        correct_answers INTEGER DEFAULT 0,
        last_score INTEGER DEFAULT 0,
        best_score INTEGER DEFAULT 0,
        last_played TEXT DEFAULT '')''')
    conn.commit()
    conn.close()
    print("✅ DB ready", flush=True)

def save_score(user_id, total, correct, score):
    conn = sqlite3.connect('pickleball_quiz.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if row:
        new_total = row[1] + total
        new_correct = row[2] + correct
        best = max(row[4], score)
        c.execute('UPDATE scores SET total_questions=?, correct_answers=?, last_score=?, best_score=?, last_played=datetime(\'now\') WHERE user_id=?',
            (new_total, new_correct, score, best, user_id))
    else:
        c.execute('INSERT INTO scores VALUES (?,?,?,?,?,datetime(\'now\'))',
            (user_id, total, correct, score, score))
    conn.commit()
    conn.close()

def get_score(user_id):
    conn = sqlite3.connect('pickleball_quiz.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'total': row[1], 'correct': row[2], 'last_score': row[3], 'best_score': row[4]}
    return None

def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['questions']

class QuizButton(Button):
    def __init__(self, option_idx, question_id, user_id):
        super().__init__(
            label=f"選項 {chr(65+option_idx)}",
            style=discord.ButtonStyle.primary,
            emoji=chr(0x1F1E6+option_idx),
            custom_id=f"q:{user_id}:{question_id}:{option_idx}"
        )
        self.option_idx = option_idx
        self.question_id = question_id
        self.user_id = user_id
    
    async def callback(self, interaction: discord.Interaction):
        try:
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message("❌ 請使用 `/pickleball start` 開始你自己的測驗！", ephemeral=True)
                return
            
            # Load questions
            questions = load_questions()
            question = next((q for q in questions if q['id'] == self.question_id), None)
            if not question:
                await interaction.response.send_message("❌ 題目找不到", ephemeral=True)
                return
            
            is_correct = (self.option_idx == question['correct'])
            
            # Send result
            if is_correct:
                result_text = f"✅ **正確！**\n\n{question['explanation']}"
            else:
                correct_text = question['options'][question['correct']]
                result_text = f"❌ **錯誤！**\n\n正確答案：{correct_text}\n\n{question['explanation']}"
            
            await interaction.response.send_message(result_text)
            
        except Exception as e:
            print(f"❌ Error: {e}", flush=True)
            traceback.print_exc()
            try:
                await interaction.followup.send(f"❌ 錯誤：{str(e)}", ephemeral=True)
            except:
                pass

@bot.tree.command(name="pickleball", description="Pickleball 教練認證模擬考試")
async def pickleball(interaction: discord.Interaction, action: str = "start", num_questions: int = 10):
    try:
        user_id = str(interaction.user.id)
        print(f"🎾 /pickleball {action} by {interaction.user.name}", flush=True)
        
        if action == "start":
            questions = load_questions()
            
            # Select random questions
            selected = random.sample(questions, min(num_questions, len(questions)))
            
            # Start message
            intro = f"""🎾 **Pickleball 教練認證模擬考試** 🎾

📋 測驗說明：
- 題目數量：{len(selected)} 題
- 及格分數：70%
- 範疇：規則、計分、場地、技術、教練知識

請點擊下方按鈕開始答題！

⏱️ 每題限時 30 秒
"""
            
            view = View(timeout=None)
            start_btn = Button(label="開始測驗", style=discord.ButtonStyle.success, 
                              emoji="🎾", custom_id=f"start:{user_id}")
            
            async def start_callback(i):
                if str(i.user.id) != user_id:
                    await i.response.send_message("❌ 這不是你的測驗！", ephemeral=True)
                    return
                
                # Send first question
                await send_question(i, selected, 0, user_id)
            
            start_btn.callback = start_callback
            view.add_item(start_btn)
            
            await interaction.response.send_message(intro, view=view)
            
        elif action == "status":
            score = get_score(user_id)
            if not score:
                await interaction.response.send_message("❌ 你尚未進行過測驗！使用 `/pickleball start` 開始", ephemeral=True)
                return
            
            accuracy = (score['correct'] / score['total'] * 100) if score['total'] > 0 else 0
            
            embed = discord.Embed(title="📊 你的統計", color=discord.Color.green())
            embed.add_field(name="🎯 總題目數", value=str(score['total']))
            embed.add_field(name="✅ 正確答案", value=str(score['correct']))
            embed.add_field(name="📈 準確率", value=f"{accuracy:.1f}%")
            embed.add_field(name="🏆 最佳成績", value=f"{score['best_score']}%")
            embed.add_field(name="📝 最後測驗", value=str(score['last_score']) + "%")
            
            await interaction.response.send_message(embed=embed)
            
        elif action == "leaderboard":
            conn = sqlite3.connect('pickleball_quiz.db')
            c = conn.cursor()
            c.execute('SELECT user_id, best_score, correct, total FROM scores ORDER BY best_score DESC LIMIT 10')
            rows = c.fetchall()
            conn.close()
            
            if not rows:
                await interaction.response.send_message("📊 暫時未有排行榜數據", ephemeral=True)
                return
            
            leaderboard = "🏆 **Pickleball 教練認證 - 排行榜** 🏆\n\n"
            for idx, row in enumerate(rows, 1):
                user = await bot.fetch_user(int(row[0]))
                accuracy = (row[2] / row[3] * 100) if row[3] > 0 else 0
                leaderboard += f"{idx}. {user.name} - 🏆 {row[1]}% (準確率 {accuracy:.1f}%)\n"
            
            await interaction.response.send_message(leaderboard)
            
    except Exception as e:
        print(f"❌ Command error: {e}", flush=True)
        traceback.print_exc()
        await interaction.response.send_message(f"❌ 錯誤：{str(e)}", ephemeral=True)

async def send_question(interaction, questions, idx, user_id):
    if idx >= len(questions):
        # Quiz complete
        await show_results(interaction, questions, user_id)
        return
    
    question = questions[idx]
    
    # Build question text
    options_text = ""
    for i, opt in enumerate(question['options']):
        options_text += f"{chr(0x1F1E6+i)} {opt}\n"
    
    question_text = f"""🎾 **第 {idx+1}/{len(questions)} 題**

{question['question']}

{options_text}
"""
    
    view = View(timeout=30)
    for i in range(len(question['options'])):
        btn = QuizButton(i, question['id'], user_id)
        
        async def button_callback(i, opt_idx=i, q_idx=idx):
            if str(i.user.id) != user_id:
                await i.response.send_message("❌ 這不是你的測驗！", ephemeral=True)
                return
            
            is_correct = (opt_idx == question['correct'])
            
            if is_correct:
                result_text = f"✅ **正確！**\n\n{question['explanation']}"
            else:
                correct_text = question['options'][question['correct']]
                result_text = f"❌ **錯誤！**\n\n正確答案：{correct_text}\n\n{question['explanation']}"
            
            await i.response.send_message(result_text)
            
            # Next question after delay
            await asyncio.sleep(3)
            await send_question(i, questions, q_idx+1, user_id)
        
        btn.callback = button_callback
        view.add_item(btn)
    
    await interaction.followup.send(question_text, view=view)

async def show_results(interaction, questions, user_id):
    # Calculate score (placeholder - need to track answers)
    score = 85  # Placeholder
    save_score(user_id, len(questions), int(len(questions)*0.85), score)
    
    result_text = f"""🎉 **測驗完成！** 🎉

📊 你的成績：
- 正確：{int(len(questions)*0.85)}/{len(questions)}
- 分數：{score}%

{"✅ 及格！" if score >= 70 else "❌ 未及格，再試一次！"}

使用 `/pickleball status` 查看你的統計
使用 `/pickleball start` 再試一次
"""
    
    await interaction.followup.send(result_text)

@bot.event
async def on_ready():
    print(f'{bot.user} logged in!', flush=True)
    init_db()
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands', flush=True)
    except Exception as e:
        print(f'❌ Sync: {e}', flush=True)

import asyncio
bot.run(os.getenv('DISCORD_TOKEN'))
