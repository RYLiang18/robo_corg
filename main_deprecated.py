import os
import json
import pprint

import discord
from discord.ext import tasks, commands
from discord.utils import get

from twitch_aux import Twitch_Aux
from twilio_aux import Twilio_Aux

from sqlalchemy.orm import sessionmaker

pp = pprint.PrettyPrinter(indent=2)

# intents allow giich_bot to subscribe to specific buckets of events
# https://discordpy.readthedocs.io/en/stable/intents.html#:~:text=In%20version%201.5%20comes%20the,attribute%20of%20the%20Intents%20documentation.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

twitch_username = "Enviosity"
twilio_client = Twilio_Aux([os.environ.get("phone_num_1")])

@bot.event
async def on_ready():
    channel = bot.get_channel(844388150447964160)

    @tasks.loop(seconds=10)
    async def live_notifs_loop():
        streamer = Twitch_Aux(twitch_username)

        # get my discord user
        giich = bot.get_user(
            int(os.environ.get("my_discord_id"))
        )

        # read from `whos_live.json` to see my most recent status
        f = open('most_recent_status.json')
        most_recent_status_data = json.load(f)
        giich_status = most_recent_status_data["thegiich"]

        print("reached here")
        print(streamer.is_live)
        if streamer.is_live and giich_status is False:
            print("reeeeeeeeeeee")
            
            await channel.send(
                f":red_circle: **LIVE**\n {twitch_username} is now streaming \"{streamer.title}\" on Twitch!"
                f":\nPlaying {streamer.game}"
            )
            print(f"{giich} started streaming. Sending a notification")

            # updating `most_recent_status.json` to true!
            most_recent_status_data["thegiich"] = True
            new_most_recent_status_data = json.dumps(
                most_recent_status_data, indent=4
            )
            with open("most_recent_status.json", "w") as outfile:
                outfile.write(new_most_recent_status_data)
            
            # >>>>>> TWILIO THINGY >>>>>>
            twilio_client.send_message()
            # <<<<<<<<<<<<<<<<<<<<<<<<<<

        elif streamer.is_live is False and giich_status is True:
            # delete the is streaming message.
            async for message in channel.history(limit=10):
                if str(giich.mention) in message.content and "is now streaming" in message.content:
                    await message.delete() 

            # revert `most_recent_status.json` to false
            most_recent_status_data["thegiich"] = False
            new_most_recent_status_data = json.dumps(
                most_recent_status_data, indent=4
            )
            with open("most_recent_status.json", "w") as outfile:
                outfile.write(new_most_recent_status_data)
    
    live_notifs_loop.start()


print("server running")
# robo-corg bot api key
TOKEN = os.environ.get("discord_key_2")
bot.run(TOKEN)