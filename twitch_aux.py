from twitchAPI.twitch import Twitch
import os

class Twitch_Aux():
    def __init__(self, twitch_name_in) -> None:
        # >>> Authentication with Twitch API >>>
        client_id = os.environ.get("twitch_id_1")
        client_secret = os.environ.get("twitch_secret_1")

        self.twitch = Twitch(client_id, client_secret)
        self.twitch.authenticate_app([])
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        
        self.twitch_name = twitch_name_in
        self.is_live = False
        self.stream_info = None
        self.game = None
        self.title = None

        self.init_helper()

        if self.is_live:
            self.game = self.stream_info[0]['game_name']
            self.title = self.stream_info[0]['title']


    def init_helper(self):
        try:
            user_id = user_id = self.twitch.get_users(
                logins=[self.twitch_name]
            )['data'][0]['id']
            self.stream_info = self.twitch.get_streams(user_id=user_id)['data']
            self.is_live = len(self.stream_info) >= 1
        except IndexError:
            self.is_live = False
            self.stream_info = None