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
# ////////////////////////////////////////////////////////

@bot.event
async def on_ready():
    channel = bot.get_channel(844388150447964160)

    @tasks.loop(seconds=60)
    async def live_notifs_loop():
        print("initiating loop")

        session = Session()
        select_streamers = select(StreamerModel).order_by(StreamerModel.id)
        for row in session.execute(select_streamers):
            sm : StreamerModel = row.StreamerModel
            streamer : Twitch_Aux = Twitch_Aux(sm.twitch_name)

            # current streamer has just gone live or has just gone offline
            if sm.is_live != streamer.is_live:
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
                        f"{streamer.twitch_name} is now streaming \"{streamer.title}!\"\n"
                        f"Playing {streamer.game}\n"
                        f"Go check it out on {streamer.get_stream_link()}\n"
                    )
                else:
                    await channel.send(
                        f":octagonal_sign: **STREAM OFFLINE**\n"
                        f"{streamer.twitch_name} is now offline"
                    )
                
                twilio_aux.send_messages(streamer)

                # update STREAMER_TBL
                sm.is_live = not sm.is_live
                session.commit()
        session.close()
    live_notifs_loop.start()

@bot.command(
    name='subscribeTo', 
    help="Receive text notifications when a specified streamer goes live",
)
async def subscribe_to(ctx, twitch_name):
    print("trying to subscribe")
    session = Session()
    twilio_aux = Twilio_Aux()
    sender_id = str(ctx.author.id)

    # query Streamer with 'twitch_name' from STREAMER_TBL
    streamer : StreamerModel = session.query(StreamerModel).filter(
        StreamerModel.twitch_name.ilike(f"%{twitch_name}%")
    ).first()

    # query Subscriber with 'sender_id' from SUBSCRIBER_TBL
    subscriber: SubscriberModel = session.query(SubscriberModel).filter(
        SubscriberModel.discord_id.ilike(f"%{sender_id}%")
    ).first()

    if streamer is not None:
        if subscriber is not None:
            streamer.subscribers.append(subscriber)
            ctx.send("done")
        else:
            # new subscriber,
            # dm for phone number
            await ctx.author.send(
                f"To receive text notifications for {streamer.twitch_name}, please enter your phone number\n"
                f"robo-corg promises to keep this information confidential!"
            )

            resp = (
                await bot.wait_for('message', check=check_phone_number_in_dms)
            ).content
            phone_number = extract_phone_number(resp)
            
            # creating new subscriber based on schema and adding relationship
            # to STREAMBER_TBL
            new_sub = SubscriberModel(
                phone_number = phone_number,
                discord_id = str(ctx.author.id)
            )
            streamer.subscribers.append(new_sub)
            twilio_aux.send_custom_message(
                phone_number, 
                f"You are now subscribed to {streamer.twitch_name}!"
            )
    else:
        await ctx.send(
            f"oops, looks like {twitch_name} is not yet registered with robo-corg!"
        )
    session.commit()
    session.close()

@bot.command(
    name="addStreamer",
    help="add a streamer to configure robo-corg to send a message whenever said streamer goes live on Twitch!"
)
async def add_streamer(ctx, twitch_name):
    # checking that streamer exists
    streamer: Twitch_Aux = Twitch_Aux(twitch_name)

    if streamer.stream_info is None:
        await ctx.send(
            f"shieee, there isn't a twitch streamer named {twitch_name}\n"
        )
    else:
        session = Session()
        sm = StreamerModel(
            twitch_name = streamer.twitch_name,
            is_live = False
        )

        session.add(sm)
        session.commit()
        session.close()

        await ctx.send(
            f"{twitch_name} has been added to the system!"
        )



TOKEN = get_docker_secret('discord_token')

print("SERVER IS RUNNING!")
bot.run(TOKEN)