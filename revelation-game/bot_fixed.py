import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import json, sqlite3, os

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

class ChoiceButton(Button):
    def __init__(self, choice, user_id, chapter, scene_id, scores):
        super().__init__(
            label=choice['text'][:50],
            style=discord.ButtonStyle.primary,
            emoji=choice['emoji'],
            custom_id=f"g_{user_id}_{scene_id}_{choice['text'][:15]}"
        )
        self.choice = choice
        self.user_id = user_id
        self.chapter = chapter
        self.scene_id = scene_id
        self.scores = scores

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Start your own game with `/revelation start`", ephemeral=True)
            return

        try:
            print(f"🎮 Button clicked: {self.choice['text'][:20]} by {interaction.user.name}")
            
            # Update scores
            new_scores = {
                'love': self.scores['love'] + self.choice['effects']['love'],
                'truth': self.scores['truth'] + self.choice['effects']['truth'],
                'afterland': self.scores['afterland'] + self.choice['effects']['afterland']
            }
            
            # Save progress
            progress = get_progress(self.user_id)
            choices_list = progress['choices'] if progress else []
            choices_list.append(self.choice['text'])
            save(self.user_id, self.chapter['chapter'], self.choice['next'],
                 new_scores['love'], new_scores['truth'], new_scores['afterland'], choices_list)
            
            # Find next scene
            next_scene = next((s for s in self.chapter['scenes'] if s['id'] == self.choice['next']), None)
            
            if next_scene:
                stats = f"❤️ {new_scores['love']} | 🔍 {new_scores['truth']} | 🌐 {new_scores['afterland']}"
                
                embed = discord.Embed(
                    title="🌊 啓示路",
                    description=next_scene['text'],
                    color=discord.Color.purple()
                )
                embed.set_footer(text=stats)
                
                if next_scene.get('choices'):
                    # Create FRESH view for next scene
                    view = View(timeout=600)
                    for c in next_scene['choices']:
                        btn = ChoiceButton(c, self.user_id, self.chapter, self.choice['next'], new_scores)
                        view.add_item(btn)
                    await interaction.response.edit_message(embed=embed, view=view)
                    print(f"✅ Next scene: {self.choice['next']}, {len(next_scene['choices'])} choices")
                else:
                    await interaction.response.edit_message(embed=embed, view=None)
                    print(f"✅ End of chapter")
            else:
                await interaction.response.send_message("❌ Scene not found. Use `/revelation start`", ephemeral=True)
                print(f"❌ Scene not found: {self.choice['next']}")
                
        except discord.errors.NotFound:
            print(f"⏰ Interaction expired")
            await interaction.followup.send("⏰ Session expired! Use `/revelation start` to restart", ephemeral=True)
        except Exception as e:
            print(f"❌ Button error: {e}")
            await interaction.followup.send(f"❌ Error: {str(e)}\nUse `/revelation start` to restart", ephemeral=True)

@bot.tree.command(name="revelation", description="Play game")
async def revelation(interaction: discord.Interaction, action: str = "start"):
    try:
        user_id = str(interaction.user.id)
        print(f"🎮 /revelation {action} by {interaction.user.name} ({user_id})")
        
        if action == "start":
            chapter = load_chapter(1)
            if not chapter:
                await interaction.response.send_message("❌ Script not found", ephemeral=True)
                return
            
            save(user_id, 1, 'scene_0', 0, 0, 0, [])
            scene = chapter['scenes'][0]
            scores = {'love': 0, 'truth': 0, 'afterland': 0}
            
            embed = discord.Embed(
                title="🌊 啓示路：樂土之門",
                description=scene['text'],
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"🔘 Player: {interaction.user.name} | ❤️ 0 | 🔍 0 | 🌐 0")
            
            view = View(timeout=600)
            for choice in scene['choices']:
                btn = ChoiceButton(choice, user_id, chapter, 'scene_0', scores)
                view.add_item(btn)
            
            await interaction.response.send_message(embed=embed, view=view)
            print(f"✅ Game started: {len(scene['choices'])} choices")
            
        elif action == "status":
            progress = get_progress(user_id)
            if not progress:
                await interaction.response.send_message("❌ No progress. Use `/revelation start`", ephemeral=True)
                return
            embed = discord.Embed(title="📊 Status", color=discord.Color.purple())
            embed.add_field(name="Chapter", value=f"{progress['chapter']}")
            embed.add_field(name="❤️ Love", value=str(progress['love']))
            embed.add_field(name="🔍 Truth", value=str(progress['truth']))
            embed.add_field(name="🌐 Afterland", value=str(progress['afterland']))
            await interaction.response.send_message(embed=embed)
            
    except Exception as e:
        print(f"❌ Command error: {e}")
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="revelation_continue", description="Continue game")
async def revelation_continue(interaction: discord.Interaction):
    try:
        user_id = str(interaction.user.id)
        progress = get_progress(user_id)
        
        if not progress:
            await interaction.response.send_message("❌ No progress. Use `/revelation start`", ephemeral=True)
            return
        
        chapter = load_chapter(progress['chapter'])
        if not chapter:
            await interaction.response.send_message("❌ Script not found", ephemeral=True)
            return
        
        scene = next((s for s in chapter['scenes'] if s['id'] == progress['scene']), None)
        if not scene:
            await interaction.response.send_message("❌ Scene not found", ephemeral=True)
            return
        
        scores = {'love': progress['love'], 'truth': progress['truth'], 'afterland': progress['afterland']}
        
        embed = discord.Embed(title="🌊 啓示路", description=scene['text'], color=discord.Color.purple())
        embed.set_footer(text=f"❤️ {scores['love']} | 🔍 {scores['truth']} | 🌐 {scores['afterland']}")
        
        if scene.get('choices'):
            view = View(timeout=600)
            for i, choice in enumerate(scene['choices']):
                btn = ChoiceButton(choice, user_id, chapter, progress['scene'], scores)
                view.add_item(btn)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message(embed=embed, view=None)
        
        print(f"✅ Game continued for {interaction.user.name} at {progress['scene']}")
        
    except Exception as e:
        print(f"❌ Continue error: {e}")
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="testbtn", description="Test")
async def testbtn(interaction: discord.Interaction):
    view = View(timeout=600)
    async def cb(i: discord.Interaction):
        await i.response.send_message("✅ Works!", ephemeral=True)
    btn = Button(label="CLICK", style=discord.ButtonStyle.success, custom_id=f"t_{interaction.user.id}")
    btn.callback = cb
    view.add_item(btn)
    embed = discord.Embed(title="🔧 Test", description="Click button", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print(f'{bot.user} logged in!')
    init_db()
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands')
    except Exception as e:
        print(f'❌ Sync error: {e}')

bot.run(os.getenv('DISCORD_TOKEN'))
