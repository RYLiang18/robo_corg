from twilio.rest import Client
from aux.twitch_aux import Twitch_Aux
from typing import Dict
import os
from get_docker_secret import get_docker_secret


class Twilio_Aux():
    def __init__(self, phone_nos_in: Dict[str, str] = None):
        # >>> Authentication with Twilio API >>>
        # account_sid = os.environ['twilio_account_sid']
        # auth_token = os.environ['twilio_auth_token']
        account_sid = get_docker_secret('twilio_sid')
        auth_token = get_docker_secret('twilio_auth_token')

        self.client = Client(account_sid, auth_token)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        self.phone_nos = phone_nos_in
        self.twilio_phone = '19549940698'

    
    def send_messages(self, streamer: Twitch_Aux):
        for phone_number, receiver_name in self.phone_nos.items():
            body = ""
            if streamer.is_live:
                body = (
                    f"🤖beep boop greetings {receiver_name} robo-corg is here🤖;\n"
                    f"{streamer.twitch_name} is now streaming \"{streamer.title}\"\n"
                    f"Playing {streamer.game}\n"
                    f"Go check it out on {streamer.get_stream_link()}\n"
                )
            else:
                body = (
                    f"beep boop {streamer.title} is now offline\n"
                )
            
            self.client.messages.create(
                body = body,
                from_= self.twilio_phone,
                to = phone_number
            )

    def send_custom_message(self, phone_number: str, body: str):
        self.client.messages.create(
            body = body,
            from_= phone_number,
            to = phone_number
        )
        