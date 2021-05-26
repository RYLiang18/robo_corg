import os
import json
import discord
import requests
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

TOKEN = os.getenv('TESTINGMF_DISCORD_TOKEN')

# Authentication with Twitch API.
client_id = "tqanfnani3tygk9a9esl8conhnaz6wj"
client_secret = "tqanfnani3tygk9a9esl8conhnaz6wj"
twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"
API_HEADERS = {
    'Client-ID': client_id,
    'Accept': 'application/vnd.twitchtv.v5+json',
}


# Returns true if online, false if not.
def checkuser(user):
    try:
        userid = twitch.get_users(logins=[user])['data'][0]['id']
        url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
        try:
            req = requests.Session().get(url, headers=API_HEADERS)
            jsondata = req.json()
            if 'stream' in jsondata:
                if jsondata['stream'] is not None:
                    return True
                else:
                    return False
        except Exception as e:
            print("Error checking user: ", e)
            return False
    except IndexError:
        return False


# Executes when bot is started
@bot.event
async def on_ready():
    # Defines a loop that will run every 10 seconds (checks for live users every 10 seconds).
    @tasks.loop(seconds=10)
    async def live_notifs_loop():
        # Opens and reads the json file
        with open('streamers.json', 'r') as file:
            streamers = json.loads(file.read())
        # Makes sure the json isn't empty before continuing.
        if streamers is not None:
            # Gets the guild, 'twitch streams' channel, and streaming role.
            guild = bot.get_guild(1234567890)
            channel = bot.get_channel(1234567890)
            role = get(guild.roles, id=1234567890)
            # Loops through the json and gets the key,value which in this case is the user_id and twitch_name of
            # every item in the json.
            for user_id, twitch_name in streamers.items():
                # Takes the given twitch_name and checks it using the checkuser function to see if they're live.
                # Returns either true or false.
                status = checkuser(twitch_name)
                # Gets the user using the collected user_id in the json
                user = bot.get_user(int(user_id))
                # Makes sure they're live
                if status is True:
                    # Checks to see if the live message has already been sent.
                    async for message in channel.history(limit=200):
                        # If it has, break the loop (do nothing).
                        if str(user.mention) in message.content and "is now streaming" in message.content:
                            break
                        # If it hasn't, assign them the streaming role and send the message.
                        else:
                            # Gets all the members in your guild.
                            async for member in guild.fetch_members(limit=None):
                                # If one of the id's of the members in your guild matches the one from the json and
                                # they're live, give them the streaming role.
                                if member.id == int(user_id):
                                    await member.add_roles(role)
                            # Sends the live notification to the 'twitch streams' channel then breaks the loop.
                            await channel.send(
                                f":red_circle: **LIVE**\n{user.mention} is now streaming on Twitch!"
                                f"\nhttps://www.twitch.tv/{twitch_name}")
                            print(f"{user} started streaming. Sending a notification.")
                            break
                # If they aren't live do this:
                else:
                    # Gets all the members in your guild.
                    async for member in guild.fetch_members(limit=None):
                        # If one of the id's of the members in your guild matches the one from the json and they're not
                        # live, remove the streaming role.
                        if member.id == int(user_id):
                            await member.remove_roles(role)
                    # Checks to see if the live notification was sent.
                    async for message in channel.history(limit=200):
                        # If it was, delete it.
                        if str(user.mention) in message.content and "is now streaming" in message.content:
                            await message.delete()
    # Start your loop.
    live_notifs_loop.start()


# Command to add Twitch usernames to the json.
@bot.command(name='addtwitch', help='Adds your Twitch to the live notifs.', pass_context=True)
async def add_twitch(ctx, twitch_name):
    # Opens and reads the json file.
    with open('streamers.json', 'r') as file:
        streamers = json.loads(file.read())
    
    # Gets the users id that called the command.
    user_id = ctx.author.id
    # Assigns their given twitch_name to their discord id and adds it to the streamers.json.
    streamers[user_id] = twitch_name
    
    # Adds the changes we made to the json file.
    with open('streamers.json', 'w') as file:
        file.write(json.dumps(streamers))
    # Tells the user it worked.
    await ctx.send(f"Added {twitch_name} for {ctx.author} to the notifications list.")


print('Server Running')
bot.run(TOKEN)