import os
import pprint

# discord.py imports
import discord
from discord.ext import tasks, commands
from discord.utils import get

# aux imports
from aux.twitch_aux import Twitch_Aux
from aux.twilio_aux import Twilio_Aux

# sqlalchemy and database imports
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database.models import (
    StreamerModel, SubscriberModel
)


# ///////////////////// STARTING UP /////////////////////
pp = pprint.PrettyPrinter(indent=2)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# connecting the database
db_pwd = os.environ.get("mysql_root_pwd")
engine = create_engine(
    f'mysql+mysqlconnector://root:{db_pwd}@localhost/robocorg'
)
# ////////////////////////////////////////////////////////

@bot.event
async def on_ready():
    channel = bot.get_channel(844388150447964160)

    @tasks.loop(seconds=60)
    async def live_notifs_loop():
        Session = sessionmaker(bind=engine)
        session = Session()
        select_streamers = select(StreamerModel).order_by(StreamerModel.id)
        for row in session.execute(select_streamers):
            sm : StreamerModel = row.StreamerModel
            streamer : Twitch_Aux = Twitch_Aux(sm.twitch_name)

            # current streamer has just gone live or has just gone offline
            if sm.is_live != streamer.is_live:
                streamer_mention = f"<@{sm.discord_id}>"

                subscriber_dict = dict()
                for subscriber in sm.subscribers:
                    sub_phone = subscriber.phone_number
                    sub_name = bot.get_user(int(subscriber.discord_id)).name
                    subscriber_dict[sub_phone] = sub_name

                pp.pprint(subscriber_dict)
                twilio_aux = Twilio_Aux(subscriber_dict)

                if streamer.is_live is True:                 
                    await channel.send(
                        f":red_circle: **TWITCH LIVE**\n"
                        f"{streamer_mention} is now streaming \"{streamer.title}!\"\n"
                        f"Playing {streamer.game}\n"
                        f"Go check it out on {streamer.get_stream_link()}\n"
                    )
                else:
                    await channel.send(
                        f":octagonal_sign: **STREAM OFFLINE**\n"
                        f"{streamer_mention} is now offline"
                    )
                
                twilio_aux.send_messages(streamer)

                # update STREAMER_TBL
                sm.is_live = not sm.is_live
                session.commit()
        session.close()
    live_notifs_loop.start()

print("server running")
# robo-corg bot api key
TOKEN = os.environ.get("discord_key_2")
bot.run(TOKEN)