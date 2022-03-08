from discord.ext import commands, tasks
from aux.twitch_aux import Twitch_Aux

from database.models import StreamerModel
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
                # subscriber_dict = dict()
                # for subscruber in db_streamer

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

def setup(client):
    client.add_cog(Twitch_Notifications(client))