from twitchAPI.twitch import Twitch
import os
import pprint
pp = pprint.PrettyPrinter(indent=2)


twitch_username = "lilypichu"

client_id = os.environ.get("twitch_id_1")
client_secret = os.environ.get("twitch_secret_1")

twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])

def check_user(user):
    try:
        user_id = twitch.get_users(logins=[user])['data'][0]['id']
        streams = twitch.get_streams(user_id=user_id)['data']

        pp.pprint(twitch.get_streams(user_id=user_id)['data'])
        return len(streams) >= 1
    except IndexError:
        return False

check_user(twitch_username)