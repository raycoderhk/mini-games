import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import json, sqlite3, os, traceback

load_dotenv()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

# Global game state
games = {}

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
    print("✅ DB ready", flush=True)

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

def format_choices(choices):
    if not choices:
        return ""
    text = "\n\n**━━━━━━━━━━━━━━━━━━━━**\n**請選擇：**\n"
    for c in choices:
        text += f"{c['emoji']} {c['text']}\n"
    return text

class StoryButton(Button):
    def __init__(self, choice, user_id, chapter_num, current_scene, next_scene, effects):
        super().__init__(
            label=choice['text'][:50],
            style=discord.ButtonStyle.primary,
            emoji=choice['emoji'],
            custom_id=f"story:{user_id}:{next_scene}"
        )
        self.choice_text = choice['text']
        self.user_id = user_id
        self.chapter_num = chapter_num
        self.current_scene = current_scene
        self.next_scene = next_scene
        self.effects = effects
    
    async def callback(self, interaction: discord.Interaction):
        try:
            print(f"🎮 Click: {self.choice_text[:20]} by {interaction.user.name}", flush=True)
            
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message("❌ Use `/revelation start`", ephemeral=True)
                return
            
            # Get current progress
            progress = get_progress(self.user_id)
            if not progress:
                await interaction.response.send_message("❌ Game not found", ephemeral=True)
                return
            
            # Update scores
            new_love = progress['love'] + self.effects['love']
            new_truth = progress['truth'] + self.effects['truth']
            new_afterland = progress['afterland'] + self.effects['afterland']
            
            # Save progress
            choices_list = progress['choices']
            choices_list.append(self.choice_text)
            save(self.user_id, self.chapter_num, self.next_scene,
                 new_love, new_truth, new_afterland, choices_list)
            
            # Load chapter and find next scene
            chapter = load_chapter(self.chapter_num)
            next_scene_data = next((s for s in chapter['scenes'] if s['id'] == self.next_scene), None)
            
            print(f"🔍 Looking for {self.next_scene} → {'Found' if next_scene_data else 'NOT FOUND'}", flush=True)
            
            if not next_scene_data:
                await interaction.response.send_message(f"❌ Scene {self.next_scene} not found", ephemeral=True)
                return
            
            # Create embed
            stats = f"❤️ {new_love} | 🔍 {new_truth} | 🌐 {new_afterland}"
            desc = next_scene_data['text'] + format_choices(next_scene_data.get('choices', []))
            
            embed = discord.Embed(title="🌊 啓示路", description=desc, color=discord.Color.purple())
            embed.set_footer(text=stats)
            
            # Create buttons if there are choices
            if next_scene_data.get('choices'):
                view = View(timeout=None)
                for c in next_scene_data['choices']:
                    btn = StoryButton(c, self.user_id, self.chapter_num, self.next_scene, 
                                     c['next'], c['effects'])
                    view.add_item(btn)
                await interaction.response.edit_message(embed=embed, view=view)
                print(f"✅ Next: {self.next_scene} with {len(next_scene_data['choices'])} choices", flush=True)
            else:
                await interaction.response.edit_message(embed=embed, view=None)
                print(f"✅ End of chapter", flush=True)
                
        except discord.errors.NotFound:
            print(f"⏰ Interaction expired", flush=True)
            await interaction.followup.send("⏰ Expired! Use `/revelation start`", ephemeral=True)
        except Exception as e:
            print(f"❌ Button error: {e}", flush=True)
            traceback.print_exc()
            await interaction.followup.send(f"❌ {str(e)}", ephemeral=True)

@bot.tree.command(name="revelation", description="Play game")
async def revelation(interaction: discord.Interaction, action: str = "start"):
    try:
        user_id = str(interaction.user.id)
        print(f"🎮 /revelation {action} by {interaction.user.name}", flush=True)
        
        if action == "start":
            chapter = load_chapter(1)
            if not chapter:
                await interaction.response.send_message("❌ Script not found", ephemeral=True)
                return
            
            print(f"✅ Loaded chapter with {len(chapter['scenes'])} scenes", flush=True)
            
            # Reset progress
            save(user_id, 1, 'scene_0', 0, 0, 0, [])
            scene = chapter['scenes'][0]
            
            # Create embed with story text AND choices
            desc = scene['text'] + format_choices(scene.get('choices', []))
            
            embed = discord.Embed(
                title="🌊 啓示路：樂土之門",
                description=desc,
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"🔘 {interaction.user.name} | ❤️ 0 | 🔍 0 | 🌐 0")
            
            # Create buttons
            view = View(timeout=None)
            for choice in scene.get('choices', []):
                btn = StoryButton(choice, user_id, chapter['chapter'], 'scene_0',
                                 choice['next'], choice['effects'])
                view.add_item(btn)
            
            await interaction.response.send_message(embed=embed, view=view)
            print(f"✅ Game started with {len(scene.get('choices', []))} choices", flush=True)
            
        elif action == "status":
            progress = get_progress(user_id)
            if not progress:
                await interaction.response.send_message("❌ No progress", ephemeral=True)
                return
            embed = discord.Embed(title="📊 Status", color=discord.Color.purple())
            embed.add_field(name="Chapter", value=str(progress['chapter']))
            embed.add_field(name="❤️ Love", value=str(progress['love']))
            embed.add_field(name="🔍 Truth", value=str(progress['truth']))
            embed.add_field(name="🌐 Afterland", value=str(progress['afterland']))
            await interaction.response.send_message(embed=embed)
            
    except Exception as e:
        print(f"❌ Command error: {e}", flush=True)
        traceback.print_exc()
        await interaction.response.send_message(f"❌ {str(e)}", ephemeral=True)

@bot.tree.command(name="testbtn", description="Test")
async def testbtn(interaction: discord.Interaction):
    view = View(timeout=None)
    async def cb(i):
        await i.response.send_message("✅ Works!", ephemeral=True)
    btn = Button(label="CLICK", style=discord.ButtonStyle.success, custom_id=f"test:{interaction.user.id}")
    btn.callback = cb
    view.add_item(btn)
    embed = discord.Embed(title="🔧 Test", description="Click!", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print(f'{bot.user} logged in!', flush=True)
    init_db()
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands', flush=True)
    except Exception as e:
        print(f'❌ Sync: {e}', flush=True)

bot.run(os.getenv('DISCORD_TOKEN'))
