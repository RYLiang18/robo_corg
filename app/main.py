import os
import pprint
from unicodedata import name
from get_docker_secret import get_docker_secret


# discord.py imports
import discord
from discord.ext import tasks, commands
from discord.utils import get

# aux imports
from aux.twitch_aux import Twitch_Aux
from aux.twilio_aux import Twilio_Aux
from aux.other import (
    check_phone_number_in_dms,
    extract_phone_number
)

# sqlalchemy and database imports
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from database.models import (
    StreamerModel, SubscriberModel
)


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

cogs = [
    'cogs.bot',
    'cogs.twitch_notifications'
]

for cog in cogs:
    bot.load_extension(cog)

TOKEN = get_docker_secret('discord_token')

print("SERVER IS RUNNING!")
bot.run(TOKEN)