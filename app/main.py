import pprint
import sys
from get_docker_secret import get_docker_secret

# discord.py imports
import discord
from discord.ext import commands

# sqlalchemy and database imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



# ///////////////////// STARTING UP /////////////////////
pp = pprint.PrettyPrinter(indent=2)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!robocorg ', intents=intents)

# connecting the database
db_user = get_docker_secret('db_user')
db_pwd = get_docker_secret('db_pwd')

# db_pwd = os.environ.get("mysql_root_pwd")
engine = create_engine(
    f'mysql+mysqlconnector://{db_user}:{db_pwd}@db/robocorg',
)

Session = sessionmaker(bind=engine)

# add current working directory to path so we can import stuff from it
sys.path.append('.')

cogs = [
    'cogs.bot',
    'cogs.twitch_notifications'
]

for cog in cogs:
    bot.load_extension(cog)

TOKEN = get_docker_secret('discord_token')

print("SERVER IS RUNNING!")
bot.run(TOKEN)