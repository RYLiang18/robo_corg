import re
from discord import Message
import os
from cryptography.fernet import Fernet

# phone number regex from
# https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script
r = re.compile(
    r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
)
fernet_key = bytes(os.environ.get('fernet_key'), 'utf-8')
f = Fernet(fernet_key)

def check_phone_number_in_dms(msg: Message):
    """
    function to validate response when bot DMs user asking for their phone number

    :param msg: <Message> a reference to the user's response to bot DM in Discord
    :return: <bool>
    """
    if not msg.author.bot and msg.channel == msg.author.dm_channel:
        print("msg in DM channel")
        match = r.search(msg.content)
        return bool(match)
    else:
        print("msg NOT in DM channel")
        return False

def extract_phone_number(phone_number: str):
    raw_str = r.search(phone_number).group()
    numeric_filter = filter(str.isdigit, raw_str)
    return "".join(numeric_filter)

def encrypt(phone_number: str):
    return f.encrypt(bytes(phone_number, 'utf-8'))

def decrypt(encrypted_phone_number: bytes):
    return f.decrypt(encrypted_phone_number).decode('utf-8')