from twitchAPI.twitch import Twitch
import os
import pprint
pp = pprint.PrettyPrinter(indent=2)


twitch_username = "lilypichu"

client_id = os.environ.get("twitch_id_1")
client_secret = os.environ.get("twitch_secret_1")

twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])

def check_user(user):
    try:
        user_id = twitch.get_users(logins=[user])['data'][0]['id']
        streams = twitch.get_streams(user_id=user_id)['data']

        pp.pprint(twitch.get_streams(user_id=user_id)['data'])
        return len(streams) >= 1
    except IndexError:
        return False

check_user(twitch_username)

# ////////////////////////////////////////////////

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database.models import (
    StreamerModel, SubscriberModel
)

db_pwd = os.environ.get("mysql_root_pwd")
engine = create_engine(f'mysql+mysqlconnector://root:{db_pwd}@localhost/robocorg')

Session = sessionmaker(bind=engine)
session = Session()

# stmt = select(StreamerModel).order_by(StreamerModel.id)
# streamer = session.execute(stmt).first()
# streamer.is_live = not streamer.is_live
# session.commit()

name = "bruh"

streamer = session.query(StreamerModel).filter(
    StreamerModel.twitch_name.ilike(f"%{name}%")
).first()

print(streamer)
# print(streamer.is_live)

session.close()