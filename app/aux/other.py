import re
from discord import Message

# phone number regex from
# https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script
r = re.compile(
    r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
)

def check_phone_number_in_dms(msg: Message):
    if msg.channel == msg.author.dm_channel:
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

extract_phone_number("my pn is (949)3946676")