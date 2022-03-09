from discord.ext import commands, tasks
from aux.twitch_aux import Twitch_Aux
from aux.twilio_aux import Twilio_Aux
from aux.other import (
    check_phone_number_in_dms,
    extract_phone_number
)

from database.models import StreamerModel, SubscriberModel
from main import Session

from sqlalchemy import select

class Twitch_Notifications(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.listener_status = False

    @tasks.loop(seconds=60)
    async def twitch_listener(self, ctx):
        print("initiating loop")

        session = Session()
        
        select_streamers_query = select(StreamerModel).order_by(StreamerModel.id)

        for row in session.execute(select_streamers_query):
            db_streamer : StreamerModel = row.StreamerModel
            curr_streamer: Twitch_Aux = Twitch_Aux(db_streamer.twitch_name)

            if curr_streamer.is_live != db_streamer.is_live:

                # //// texting ////////////////////
                subscriber_dict = dict()
                for subscriber in db_streamer.subscribers:
                    sub_phone = subscriber.phone_number
                    sub_name = self.client.get_user(int(subscriber.discord_id)).name
                    subscriber_dict[sub_phone] = sub_name

                twilio_aux = Twilio_Aux(subscriber_dict)
                twilio_aux.send_messages(curr_streamer)
                # /////////////////////////////////

                if curr_streamer.is_live:
                    await ctx.send(
                        f"{curr_streamer.twitch_name} is now live!\n"
                        f"Go check it out on {curr_streamer.get_stream_link()}\n"
                    )
                else:
                    await ctx.send(
                        f"{curr_streamer.twitch_name} is now offline"
                    )
            
                db_streamer.is_live = curr_streamer.is_live
                session.commit()
        session.close()
    
    @commands.command()
    async def start_twitch_notifs(self, ctx):
        await ctx.send("twitch live notifications STARTING...")
        self.twitch_listener.start(ctx)
    
    @commands.command()
    async def stop_twitch_notifs(self, ctx):
        await ctx.send("twitch live notifications STOPPING...")
        self.twitch_listener.stop()

    @commands.command()
    async def subscribe_to(self, ctx, twitch_name):
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
                    await self.client.wait_for('message', check=check_phone_number_in_dms)
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

    @commands.command()
    async def add_streamer(self, ctx, twitch_name):
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

def setup(client):
    client.add_cog(Twitch_Notifications(client))