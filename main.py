# kudos to: 
# https://www.youtube.com/watch?v=AHdb8K6BHLY
# https://mystb.in/CompeteRejectedAshley.python
# 

import os
import json
import discord
import requests
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get

import pprint

pp = pprint.PrettyPrinter(indent=2)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# robo-corg bot api key
TOKEN = os.environ.get("discord_key_2")

# >>> Authentication with Twitch API >>>
client_id = os.environ.get("twitch_id_1")
client_secret = os.environ.get("twitch_secret_1")

twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# check to see if user is online
def check_user(user):
    try:
        user_id = twitch.get_users(logins=[user])['data'][0]['id']
        streams = twitch.get_streams(user_id=user_id)['data']
        return len(streams) >= 1
    except IndexError:
        return False



