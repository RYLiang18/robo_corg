import pprint
from get_docker_secret import get_docker_secret

# discord.py imports
import discord
from discord.ext import commands

# ///////////////////// STARTING UP /////////////////////
pp = pprint.PrettyPrinter(indent=2)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!robocorg ', intents=intents)

cogs = [
    'cogs.bot',
    'cogs.twitch_notifications',
    'cogs.twitch_notifications_util'
]

for cog in cogs:
    bot.load_extension(cog)

TOKEN = get_docker_secret('discord_token')

print("SERVER IS RUNNING!")
bot.run(TOKEN)