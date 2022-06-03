from twilio.rest import Client
import os


class Twilio_Aux():
    def __init__(self):
        # >>> Authentication with Twilio API >>>
        account_sid = os.environ.get('twilio_sid')
        auth_token = os.environ.get('twilio_auth_token')

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
        