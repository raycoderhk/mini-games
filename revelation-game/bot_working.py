import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import json, sqlite3, os
from datetime import datetime

load_dotenv()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

# Database
def init_db():
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        user_id TEXT PRIMARY KEY, chapter INTEGER DEFAULT 1,
        scene TEXT DEFAULT 'scene_0', love INTEGER DEFAULT 0,
        truth INTEGER DEFAULT 0, afterland INTEGER DEFAULT 0,
        choices TEXT DEFAULT '[]')''')
    conn.commit()
    conn.close()

def save(user_id, chapter, scene, love, truth, afterland, choices):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO players VALUES (?,?,?,?,?,?,?)',
        (user_id, chapter, scene, love, truth, afterland, json.dumps(choices)))
    conn.commit()
    conn.close()

def get_progress(user_id):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('SELECT * FROM players WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'chapter': row[1], 'scene': row[2], 'love': row[3], 
                'truth': row[4], 'afterland': row[5], 'choices': json.loads(row[6])}
    return None

def load_chapter(num):
    path = f'scripts/chapter_{num}.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# Simple button callback class
class ChoiceButton(Button):
    def __init__(self, choice, user_id, chapter, scores, all_choices):
        super().__init__(label=choice['text'][:45], style=discord.ButtonStyle.primary, 
                        emoji=choice['emoji'], custom_id=f"choice_{choice['text']}")
        self.choice = choice
        self.user_id = user_id
        self.chapter = chapter
        self.scores = scores
        self.all_choices = all_choices
    
    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Not your game!", ephemeral=True)
            return
        
        # Update scores
        self.scores['love'] += self.choice['effects']['love']
        self.scores['truth'] += self.choice['effects']['truth']
        self.scores['afterland'] += self.choice['effects']['afterland']
        
        # Save progress
        progress = get_progress(self.user_id)
        choices_list = progress['choices'] if progress else []
        choices_list.append(self.choice['text'])
        save(self.user_id, self.chapter['chapter'], self.choice['next'],
             self.scores['love'], self.scores['truth'], self.scores['afterland'], choices_list)
        
        # Find next scene
        next_scene = next((s for s in self.chapter['scenes'] if s['id'] == self.choice['next']), None)
        
        if next_scene:
            embed = discord.Embed(title="🌊 啓示路", description=next_scene['text'], color=discord.Color.purple())
            
            if next_scene['choices']:
                view = discord.ui.View(timeout=600)
                for c in next_scene['choices']:
                    btn = ChoiceButton(c, self.user_id, self.chapter, self.scores, next_scene['choices'])
                    view.add_item(btn)
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                await interaction.response.edit_message(embed=embed, view=None)

class GameView(View):
    def __init__(self, choices, user_id, chapter, scores):
        super().__init__(timeout=600)
        for choice in choices:
            self.add_item(ChoiceButton(choice, user_id, chapter, scores, choices))

@bot.tree.command(name="revelation", description="Play Revelation Road game")
async def revelation(interaction: discord.Interaction, action: str = "start"):
    user_id = str(interaction.user.id)
    
    if action == "start":
        chapter = load_chapter(1)
        if not chapter:
            await interaction.response.send_message("❌ Script not found", ephemeral=True)
            return
        
        save(user_id, 1, 'scene_0', 0, 0, 0, [])
        scene = chapter['scenes'][0]
        scores = {'love': 0, 'truth': 0, 'afterland': 0}
        
        embed = discord.Embed(title="🌊 啓示路：樂土之門", description=scene['text'], color=discord.Color.purple())
        embed.set_footer(text="🔘 Click buttons below")
        
        view = GameView(scene['choices'], user_id, chapter, scores)
        await interaction.response.send_message(embed=embed, view=view)
        print(f"Game started for {interaction.user.name}, sent {len(scene['choices'])} buttons")

@bot.tree.command(name="testbtn", description="Test button")
async def testbtn(interaction: discord.Interaction):
    view = View(timeout=600)
    
    async def btn_callback(interaction: discord.Interaction):
        await interaction.response.send_message("✅ BUTTON WORKS! 🎉", ephemeral=True)
        print(f"Button clicked by {interaction.user.name}")
    
    btn = Button(label="CLICK ME!", style=discord.ButtonStyle.success, emoji="🔘", custom_id="test_btn")
    btn.callback = btn_callback
    view.add_item(btn)
    
    embed = discord.Embed(title="🔧 Button Test", description="Click the button!", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=view)
    print(f"Test button sent to {interaction.user.name}")

@bot.event
async def on_ready():
    print(f'{bot.user} logged in!')
    init_db()
    synced = await bot.tree.sync()
    print(f'✅ Synced {len(synced)} commands')
    for cmd in synced:
        print(f'  /{cmd.name}')

bot.run(os.getenv('DISCORD_TOKEN'))
