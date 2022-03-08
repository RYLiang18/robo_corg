from discord.ext import commands, tasks


class Twitch_Notifications(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.listener_status = False

    @tasks.loop(seconds=10)
    async def twitch_listener(self, ctx):
        await ctx.send("loop")

    @commands.command()
    async def start_twitch_notifs(self, ctx):
        await ctx.send("twitch live notifications STARTING...")
        self.twitch_listener.start(ctx)
    
    @commands.command()
    async def stop_twitch_notifs(self, ctx):
        await ctx.send("twitch live notifications STOPPING...")
        self.twitch_listener.cancel()

    # @commands.command()
    # async def twitch_notifs_off(self, ctx):
    #     await ctx.send("twitch live notifications STOPPING...")
    #     twitch_listener.cancel()

def setup(client):
    client.add_cog(Twitch_Notifications(client))