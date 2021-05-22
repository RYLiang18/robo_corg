# shoutout to https://www.youtube.com/watch?v=gb6BWQobeWI for da code

# >>> imports >>>
import discord
from discord import Intents
from discord import Streaming
from discord.utils import get
from discord.ext import commands
# <<<<<<<<<<<<<<<

# intents allow giich_bot to subscribe to specific buckets of events
# https://discordpy.readthedocs.io/en/stable/intents.html#:~:text=In%20version%201.5%20comes%20the,attribute%20of%20the%20Intents%20documentation.
intents = Intents.all()

bot = commands.Bot(
    command_prefix='!',
    intent = intents
)

# https://discordpy.readthedocs.io/en/stable/api.html#discord.on_member_update
@bot.event
async def on_member_update(self, before, after):
    # note: `guild` means `server`
    
    # if user is still in same server after update and activity is still the same, do nothing
    if after.guild.id == 844362684307734548 and before.activity == after.activity:
        return

    