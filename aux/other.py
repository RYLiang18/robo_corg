import re
from discord import Message

# phone number regex from
# https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script
r = re.compile(
    r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
)

def checkPhoneNumber(msg: Message):
    if msg.channel == msg.author.dm_channel:
        print("msg in DM channel")
        match = r.search(msg.content)
        return bool(match)
    else:
        print("msg NOT in DM channel")
        return False

