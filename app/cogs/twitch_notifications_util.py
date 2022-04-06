from discord.ext import commands
from database import Session
from database.models import StreamerModel, SubscriberModel
from sqlalchemy import select

class Twitch_Notifications_Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def show_all_streamers(self, ctx):
        """
        *ADMIN ONLY COMMAND*
        command to print all streamers registered for Twitch Notifications
        """
        with Session() as session:
            select_streamers_query = select(StreamerModel).order_by(StreamerModel.id)
            for row in session.execute(select_streamers_query):
                db_streamer : StreamerModel = row.StreamerModel
                await ctx.send(f"{db_streamer.id} : {db_streamer.twitch_name}\n")

def setup(client):
    client.add_cog(Twitch_Notifications_Utilities(client))