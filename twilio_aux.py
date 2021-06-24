from discord import message
from main import client

def send_message():
    numbers_to_message = ['+1***REMOVED***']
    for phone_number in numbers_to_message:
        client.messages.create(
            body = 'thegiich is live wooooo',
            from_= '+19549940698',
            to = phone_number
        )
    