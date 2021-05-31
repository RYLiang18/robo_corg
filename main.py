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

# intents allow giich_bot to subscribe to specific buckets of events
# https://discordpy.readthedocs.io/en/stable/intents.html#:~:text=In%20version%201.5%20comes%20the,attribute%20of%20the%20Intents%20documentation.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

twitch_username = "thegiich"

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



@bot.event
async def on_ready():
    server = bot.get_guild(844362684307734548)
    channel = bot.get_channel(844388150447964160)

    @tasks.loop(seconds=10)
    async def live_notifs_loop():
        stream_status = check_user(twitch_username)

        # get my discord user
        giich = bot.get_user(
            int(os.environ.get("my_discord_id"))
        )

        if stream_status is True:
            notif_sent = False
            # check if stream message has been sent
            async for message in channel.history(limit=10):
                # if stream message has been sent, break out of the loop
                if str(giich.mention) in message.content and "is now streaming" in message.content:
                    notif_sent = True
                    break
               
            if not notif_sent:
                await channel.send(
                    f":red_circle: **LIVE**\n {giich.mention} is now streaming on Twitch!"
                    f"\nhttps://www.twitch.tv/{twitch_username}"
                )

                # >>>>>> CONTACT FACEBOOK MESSENGER BOT >>>>>>
                # TODO
                # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

                print(f"{giich} started streaming. Sending a notification")
        else:
            # check to see if a live notification was sent
            async for message in channel.history(limit=10):
                if str(giich.mention) in message.content and "is now streaming" in message.content:
                    await message.delete() 
    
    live_notifs_loop.start()


print("server running")
# robo-corg bot api key
TOKEN = os.environ.get("discord_key_2")
bot.run(TOKEN)