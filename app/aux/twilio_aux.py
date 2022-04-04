from twilio.rest import Client
from get_docker_secret import get_docker_secret


class Twilio_Aux():
    def __init__(self):
        # >>> Authentication with Twilio API >>>
        account_sid = get_docker_secret('twilio_sid')
        auth_token = get_docker_secret('twilio_auth_token')

        self.client = Client(account_sid, auth_token)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # self.phone_nos = phone_nos_in
        self.twilio_phone = '19549940698'

    def send_message(self, phone_number: str, body: str):
        self.client.messages.create(
            body = body,
            from_= self.twilio_phone,
            to = phone_number
        )
        