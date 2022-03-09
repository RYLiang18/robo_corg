from twitchAPI.twitch import Twitch
from get_docker_secret import get_docker_secret
import pprint
import sys

pp = pprint.PrettyPrinter(indent = 2)
pp.pprint(sys.path)

client_id = get_docker_secret('twitch_client_id')
client_secret = get_docker_secret('twitch_client_secret')
twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])


streams = twitch.get_streams()['data'][0:5]

streamers_seed = []
richard_phone_number = get_docker_secret('giich_phone_number')
richard_discord_id = '319238198670917632'

for stream in streams:
    streamers_seed.append({
        'twitch_name': stream['user_name'],
        'is_live': False
    })

subscribers_seed = [
    {
        'phone_number': richard_phone_number,
        'discord_id': richard_discord_id
    }
]

relationship_seed = [
    {
        'phone_number': richard_phone_number,
        'twitch_name': streamers_seed[0]['twitch_name']
    },
]