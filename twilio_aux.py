from twilio.rest import Client
import os

class Twilio_Aux():
    def __init__(self, phone_nos_in):
        account_sid = os.environ['twilio_account_sid']
        auth_token = os.environ['twilio_auth_token']
        self.client = Client(account_sid, auth_token)
        self.phone_nos = phone_nos_in
        self.twilio_phone = '19549940698'

    
    def send_message(self):
        for phone_number in self.phone_nos:
            self.client.messages.create(
                body = 'SOEMONE ON TWITCH is live wooooo',
                from_= self.twilio_phone,
                to = phone_number
            )
        