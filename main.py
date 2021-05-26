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

# https://dev.twitch.tv/docs/api/reference#get-streams
TWITCH_STREAM_API_ENDPOINT = "https://api.twitch.tv/helix/streams?user_id={0}"
API_HEADERS = {
    'Client-Id': client_id,
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Authorization': f"Bearer {twitch.get_app_token()}"
}
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def check_user(user):
    try:
        user_id = twitch.get_users(
            logins=[user]
        )['data'][0]['id']

        print(user_id)

        url = TWITCH_STREAM_API_ENDPOINT.format(user_id)
        # data = {"user_id" : user_id}

        # try to get active status
        try:
            req = requests.Session().get(url, headers=API_HEADERS)
            json_data = req.json()

            pp.pprint(json_data)

        except Exception as e:
            pp.pprint(f"Error checking user: {e}")
            return False

    except IndexError:
        return False

check_user("thegiich")