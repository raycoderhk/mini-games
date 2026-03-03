import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import json, sqlite3, os, traceback

load_dotenv()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

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
    def __init__(self, choice, user_id, chapter_num, current_scene, choice_idx):
        super().__init__(
            label=choice['text'][:50],
            style=discord.ButtonStyle.primary,
            emoji=choice['emoji'],
            custom_id=f"s:{user_id}:{current_scene}:{choice_idx}"
        )
        self.choice_text = choice['text']
        self.user_id = user_id
        self.chapter_num = chapter_num
        self.current_scene = current_scene
        self.choice_idx = choice_idx
        self.next_scene = choice['next']
        self.effects = choice['effects']
    
    async def callback(self, interaction: discord.Interaction):
        try:
            print(f"🎮 Click: {self.choice_text[:20]} by {interaction.user.name}", flush=True)
            
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message("❌ Use `/revelation start`", ephemeral=True)
                return
            
            progress = get_progress(self.user_id)
            if not progress:
                await interaction.response.send_message("❌ Game not found", ephemeral=True)
                return
            
            new_love = progress['love'] + self.effects['love']
            new_truth = progress['truth'] + self.effects['truth']
            new_afterland = progress['afterland'] + self.effects['afterland']
            
            choices_list = progress['choices']
            choices_list.append(self.choice_text)
            save(self.user_id, self.chapter_num, self.next_scene,
                 new_love, new_truth, new_afterland, choices_list)
            print(f"💾 Saved", flush=True)
            
            chapter = load_chapter(self.chapter_num)
            next_scene_data = next((s for s in chapter['scenes'] if s['id'] == self.next_scene), None)
            
            print(f"🔍 Next: {self.next_scene} → {'Found' if next_scene_data else 'NOT FOUND'}", flush=True)
            
            if not next_scene_data:
                await interaction.response.send_message(f"❌ Scene not found", ephemeral=True)
                return
            
            stats = f"❤️ {new_love} | 🔍 {new_truth} | 🌐 {new_afterland}"
            desc = next_scene_data['text'] + format_choices(next_scene_data.get('choices', []))
            
            embed = discord.Embed(title="🌊 啓示路", description=desc, color=discord.Color.purple())
            embed.set_footer(text=stats)
            
            if next_scene_data.get('choices'):
                view = View(timeout=None)
                for idx, c in enumerate(next_scene_data['choices']):
                    btn = StoryButton(c, self.user_id, self.chapter_num, self.next_scene, idx)
                    view.add_item(btn)
                await interaction.response.edit_message(embed=embed, view=view)
                print(f"✅ Next: {self.next_scene}", flush=True)
            else:
                await interaction.response.edit_message(embed=embed, view=None)
                print(f"✅ End", flush=True)
                
        except discord.errors.InteractionResponded:
            print(f"⚠️ Already responded", flush=True)
            pass
        except discord.errors.NotFound as e:
            print(f"❌ NotFound: {e}", flush=True)
            print(f"Traceback:", flush=True)
            traceback.print_exc()
            try:
                await interaction.followup.send("⏰ Session expired! Use `/revelation start`", ephemeral=True)
            except:
                pass
        except Exception as e:
            print(f"❌ Error: {e}", flush=True)
            print(f"Traceback:", flush=True)
            traceback.print_exc()
            try:
                await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
            except:
                pass

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
            
            print(f"✅ Loaded {len(chapter['scenes'])} scenes", flush=True)
            
            save(user_id, 1, 'scene_0', 0, 0, 0, [])
            scene = chapter['scenes'][0]
            
            desc = scene['text'] + format_choices(scene.get('choices', []))
            
            embed = discord.Embed(
                title="🌊 啓示路：樂土之門",
                description=desc,
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"🔘 {interaction.user.name} | ❤️ 0 | 🔍 0 | 🌐 0")
            
            view = View(timeout=None)
            for idx, choice in enumerate(scene.get('choices', [])):
                btn = StoryButton(choice, user_id, chapter['chapter'], 'scene_0', idx)
                view.add_item(btn)
            
            await interaction.response.send_message(embed=embed, view=view)
            print(f"✅ Started", flush=True)
            
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
    btn = Button(label="CLICK", style=discord.ButtonStyle.success, custom_id=f"t:{interaction.user.id}")
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
