from main import twitch

def check_user(user):
    try:
        user_id = twitch.get_users(logins=[user])['data'][0]['id']
        streams = twitch.get_streams(user_id=user_id)['data']
        return len(streams) >= 1
    except IndexError:
        return False