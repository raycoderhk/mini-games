import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import json, sqlite3, os

load_dotenv()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())
db_ready = False

# Database
def init_db():
    global db_ready
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        user_id TEXT PRIMARY KEY, chapter INTEGER DEFAULT 1,
        scene TEXT DEFAULT 'scene_0', love INTEGER DEFAULT 0,
        truth INTEGER DEFAULT 0, afterland INTEGER DEFAULT 0,
        choices TEXT DEFAULT '[]')''')
    conn.commit()
    conn.close()
    db_ready = True
    print("✅ Database ready", flush=True)

def save(user_id, chapter, scene, love, truth, afterland, choices):
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO players VALUES (?,?,?,?,?,?,?)',
        (user_id, chapter, scene, love, truth, afterland, json.dumps(choices)))
    conn.commit()
    conn.close()

def get_progress(user_id):
    if not db_ready:
        return None
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
    text = "\n\n**━━━━━━━━━━━━━━━━━━━━**\n**請選擇：**\n"
    for c in choices:
        text += f"{c['emoji']} {c['text']}\n"
    return text

class GameView(View):
    def __init__(self, user_id, chapter, scene_id, scores):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.chapter = chapter
        self.scene_id = scene_id
        self.scores = scores
        
        scene = next((s for s in chapter['scenes'] if s['id'] == scene_id), None)
        if scene and scene.get('choices'):
            for i, choice in enumerate(scene['choices']):
                btn = Button(
                    label=choice['text'][:50],
                    style=discord.ButtonStyle.primary,
                    emoji=choice['emoji'],
                    custom_id=f"game:{user_id}:{scene_id}:{i}"
                )
                btn.callback = self.make_callback(choice)
                self.add_item(btn)
    
    def make_callback(self, choice):
        async def callback(interaction: discord.Interaction):
            try:
                print(f"🎮 Click: {choice['text'][:15]} by {interaction.user.name}", flush=True)
                
                if str(interaction.user.id) != self.user_id:
                    await interaction.response.send_message("❌ Use `/revelation start`", ephemeral=True)
                    return
                
                new_scores = {
                    'love': self.scores['love'] + choice['effects']['love'],
                    'truth': self.scores['truth'] + choice['effects']['truth'],
                    'afterland': self.scores['afterland'] + choice['effects']['afterland']
                }
                
                progress = get_progress(self.user_id)
                choices_list = progress['choices'] if progress else []
                choices_list.append(choice['text'])
                save(self.user_id, self.chapter['chapter'], choice['next'],
                     new_scores['love'], new_scores['truth'], new_scores['afterland'], choices_list)
                
                next_scene = next((s for s in self.chapter['scenes'] if s['id'] == choice['next']), None)
                
                if next_scene:
                    stats = f"❤️ {new_scores['love']} | 🔍 {new_scores['truth']} | 🌐 {new_scores['afterland']}"
                    desc = next_scene['text']
                    if next_scene.get('choices'):
                        desc += format_choices(next_scene['choices'])
                    
                    embed = discord.Embed(title="🌊 啓示路", description=desc, color=discord.Color.purple())
                    embed.set_footer(text=stats)
                    
                    if next_scene['choices']:
                        new_view = GameView(self.user_id, self.chapter, choice['next'], new_scores)
                        await interaction.response.edit_message(embed=embed, view=new_view)
                        print(f"✅ Next: {choice['next']}", flush=True)
                    else:
                        await interaction.response.edit_message(embed=embed, view=None)
                else:
                    await interaction.response.send_message("❌ Scene not found", ephemeral=True)
                    
            except discord.errors.NotFound:
                await interaction.followup.send("⏰ Expired! Use `/revelation start`", ephemeral=True)
            except Exception as e:
                print(f"❌ Error: {e}", flush=True)
                await interaction.followup.send(f"❌ {str(e)}", ephemeral=True)
        
        return callback

@bot.tree.command(name="revelation", description="Play game")
async def revelation(interaction: discord.Interaction, action: str = "start"):
    if not db_ready:
        await interaction.response.send_message("⏳ Database loading...", ephemeral=True)
        return
    
    try:
        user_id = str(interaction.user.id)
        print(f"🎮 /revelation {action} by {interaction.user.name}", flush=True)
        
        if action == "start":
            chapter = load_chapter(1)
            if not chapter:
                await interaction.response.send_message("❌ Script not found", ephemeral=True)
                return
            
            save(user_id, 1, 'scene_0', 0, 0, 0, [])
            scene = chapter['scenes'][0]
            scores = {'love': 0, 'truth': 0, 'afterland': 0}
            
            desc = scene['text']
            if scene.get('choices'):
                desc += format_choices(scene['choices'])
            
            embed = discord.Embed(title="🌊 啓示路：樂土之門", description=desc, color=discord.Color.purple())
            embed.set_footer(text=f"🔘 {interaction.user.name} | ❤️ 0 | 🔍 0 | 🌐 0")
            
            view = GameView(user_id, chapter, 'scene_0', scores)
            await interaction.response.send_message(embed=embed, view=view)
            print(f"✅ Started: {len(scene['choices'])} choices", flush=True)
            
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
        await interaction.response.send_message(f"❌ {str(e)}", ephemeral=True)

@bot.tree.command(name="revelation_continue", description="Continue")
async def revelation_continue(interaction: discord.Interaction):
    if not db_ready:
        await interaction.response.send_message("⏳ Database loading...", ephemeral=True)
        return
    
    try:
        user_id = str(interaction.user.id)
        progress = get_progress(user_id)
        if not progress:
            await interaction.response.send_message("❌ No progress", ephemeral=True)
            return
        
        chapter = load_chapter(progress['chapter'])
        scene = next((s for s in chapter['scenes'] if s['id'] == progress['scene']), None)
        if not scene:
            await interaction.response.send_message("❌ Scene not found", ephemeral=True)
            return
        
        scores = {'love': progress['love'], 'truth': progress['truth'], 'afterland': progress['afterland']}
        desc = scene['text']
        if scene.get('choices'):
            desc += format_choices(scene['choices'])
        
        embed = discord.Embed(title="🌊 啓示路", description=desc, color=discord.Color.purple())
        embed.set_footer(text=f"❤️ {scores['love']} | 🔍 {scores['truth']} | 🌐 {scores['afterland']}")
        
        if scene.get('choices'):
            view = GameView(user_id, chapter, progress['scene'], scores)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(embed=embed, view=None)
        
        print(f"✅ Continued at {progress['scene']}", flush=True)
        
    except Exception as e:
        print(f"❌ Continue error: {e}", flush=True)
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
