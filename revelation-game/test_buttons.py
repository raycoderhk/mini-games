import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

class SimpleView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    async def button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ WORKS! Button clicked!", ephemeral=True)

@bot.tree.command(name="testbtn", description="Test clickable button")
async def testbtn(interaction: discord.Interaction):
    view = SimpleView()
    button = Button(label="CLICK ME!", style=discord.ButtonStyle.success, emoji="🔘", custom_id="test_click")
    button.callback = view.button_callback
    view.add_item(button)
    
    embed = discord.Embed(title="🔧 Button Test", description="Is the button below clickable?", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=view)
    print(f"Button sent to {interaction.user.name}")

@bot.event
async def on_ready():
    print(f'{bot.user} logged in!')
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")

bot.run(os.getenv('DISCORD_TOKEN'))
