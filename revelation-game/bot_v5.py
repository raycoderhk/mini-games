import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import json, sqlite3, os, sys, traceback

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

@bot.tree.command(name="revelation", description="Play game")
async def revelation(interaction: discord.Interaction, action: str = "start"):
    try:
        user_id = str(interaction.user.id)
        print(f"🎮 /revelation {action} by {interaction.user.name}", flush=True)
        
        if action == "start":
            chapter = load_chapter(1)
            if not chapter:
                print("❌ Script not found", flush=True)
                await interaction.response.send_message("❌ Script not found", ephemeral=True)
                return
            
            print(f"✅ Loaded chapter with {len(chapter['scenes'])} scenes", flush=True)
            
            save(user_id, 1, 'scene_0', 0, 0, 0, [])
            scene = chapter['scenes'][0]
            scores = {'love': 0, 'truth': 0, 'afterland': 0}
            
            desc = scene['text'] + format_choices(scene['choices'])
            
            embed = discord.Embed(title="🌊 啓示路：樂土之門", description=desc, color=discord.Color.purple())
            embed.set_footer(text=f"🔘 {interaction.user.name} | ❤️ 0 | 🔍 0 | 🌐 0")
            
            view = View(timeout=None)
            for i, choice in enumerate(scene['choices']):
                btn = Button(label=choice['text'][:50], style=discord.ButtonStyle.primary,
                            emoji=choice['emoji'], custom_id=f"game:{user_id}:scene_0:{i}")
                
                async def make_callback(ch, sc, ch_id, scr, choice_data):
                    async def callback(interaction: discord.Interaction):
                        try:
                            print(f"🎮 Click: {choice_data['text'][:15]} by {interaction.user.name}", flush=True)
                            
                            if str(interaction.user.id) != ch_id:
                                await interaction.response.send_message("❌ Use `/revelation start`", ephemeral=True)
                                return
                            
                            new_scores = {
                                'love': scr['love'] + choice_data['effects']['love'],
                                'truth': scr['truth'] + choice_data['effects']['truth'],
                                'afterland': scr['afterland'] + choice_data['effects']['afterland']
                            }
                            
                            progress = get_progress(ch_id)
                            choices_list = progress['choices'] if progress else []
                            choices_list.append(choice_data['text'])
                            save(ch_id, ch['chapter'], choice_data['next'],
                                 new_scores['love'], new_scores['truth'], new_scores['afterland'], choices_list)
                            
                            next_scene = next((s for s in ch['scenes'] if s['id'] == choice_data['next']), None)
                            print(f"🔍 Next scene: {choice_data['next']} → {'Found' if next_scene else 'NOT FOUND'}", flush=True)
                            
                            if next_scene:
                                stats = f"❤️ {new_scores['love']} | 🔍 {new_scores['truth']} | 🌐 {new_scores['afterland']}"
                                next_desc = next_scene['text'] + format_choices(next_scene['choices'])
                                
                                embed2 = discord.Embed(title="🌊 啓示路", description=next_desc, color=discord.Color.purple())
                                embed2.set_footer(text=stats)
                                
                                if next_scene['choices']:
                                    new_view = View(timeout=None)
                                    for j, c in enumerate(next_scene['choices']):
                                        btn2 = Button(label=c['text'][:50], style=discord.ButtonStyle.primary,
                                                     emoji=c['emoji'], custom_id=f"game:{ch_id}:{choice_data['next']}:{j}")
                                        
                                        async def make_cb2(ch2, sc2, ch_id2, scr2, choice_data2):
                                            async def cb2(interaction2: discord.Interaction):
                                                try:
                                                    print(f"🎮 Click2: {choice_data2['text'][:15]} by {interaction2.user.name}", flush=True)
                                                    
                                                    if str(interaction2.user.id) != ch_id2:
                                                        await interaction2.response.send_message("❌ Use `/revelation start`", ephemeral=True)
                                                        return
                                                    
                                                    new_scores2 = {
                                                        'love': scr2['love'] + choice_data2['effects']['love'],
                                                        'truth': scr2['truth'] + choice_data2['effects']['truth'],
                                                        'afterland': scr2['afterland'] + choice_data2['effects']['afterland']
                                                    }
                                                    
                                                    progress2 = get_progress(ch_id2)
                                                    choices_list2 = progress2['choices'] if progress2 else []
                                                    choices_list2.append(choice_data2['text'])
                                                    save(ch_id2, ch2['chapter'], choice_data2['next'],
                                                         new_scores2['love'], new_scores2['truth'], new_scores2['afterland'], choices_list2)
                                                    
                                                    next_scene2 = next((s for s in ch2['scenes'] if s['id'] == choice_data2['next']), None)
                                                    print(f"🔍 Next scene2: {choice_data2['next']} → {'Found' if next_scene2 else 'NOT FOUND'}", flush=True)
                                                    
                                                    if next_scene2:
                                                        stats2 = f"❤️ {new_scores2['love']} | 🔍 {new_scores2['truth']} | 🌐 {new_scores2['afterland']}"
                                                        next_desc2 = next_scene2['text'] + format_choices(next_scene2['choices'])
                                                        
                                                        embed3 = discord.Embed(title="🌊 啓示路", description=next_desc2, color=discord.Color.purple())
                                                        embed3.set_footer(text=stats2)
                                                        
                                                        if next_scene2['choices']:
                                                            await interaction2.response.edit_message(embed=embed3, view=None)  # Simplify for now
                                                            print(f"⚠️ More scenes but simplifying view", flush=True)
                                                        else:
                                                            await interaction2.response.edit_message(embed=embed3, view=None)
                                                            print(f"✅ Chapter complete!", flush=True)
                                                    else:
                                                        await interaction2.response.send_message("❌ Scene not found", ephemeral=True)
                                                    
                                                except Exception as e:
                                                    print(f"❌ Error cb2: {e}", flush=True)
                                                    traceback.print_exc()
                                                    await interaction2.followup.send(f"❌ {str(e)}", ephemeral=True)
                                            return cb2
                                        
                                        btn2.callback = make_cb2(ch, sc, ch_id, new_scores, c)
                                        new_view.add_item(btn2)
                                    
                                    await interaction.response.edit_message(embed=embed2, view=new_view)
                                    print(f"✅ Next: {choice_data['next']}", flush=True)
                                else:
                                    await interaction.response.edit_message(embed=embed2, view=None)
                                    print(f"✅ End of chapter", flush=True)
                            else:
                                await interaction.response.send_message("❌ Scene not found", ephemeral=True)
                            
                        except discord.errors.NotFound:
                            await interaction.followup.send("⏰ Expired! Use `/revelation start`", ephemeral=True)
                        except Exception as e:
                            print(f"❌ Error: {e}", flush=True)
                            traceback.print_exc()
                            await interaction.followup.send(f"❌ {str(e)}", ephemeral=True)
                    return callback
                
                btn.callback = make_callback(chapter, scene, user_id, scores, choice)
                view.add_item(btn)
            
            await interaction.response.send_message(embed=embed, view=view)
            print(f"✅ Game started", flush=True)
            
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
