# import mysql.connector
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

from database.models import (
    base, StreamerModel, SubscriberModel, RelationshipModel
)

from seed_data import (
    streamers_seed, subscribers_seed, relationship_seed
)

# connecting the database
db_pwd = os.environ.get("mysql_root_pwd")
engine = create_engine(f'mysql+mysqlconnector://root:{db_pwd}@localhost/robocorg')

# create tables based on the models, i guess
base.metadata.drop_all(engine)
base.metadata.create_all(bind=engine)

# ///////////////////////////////////
Session = sessionmaker(bind=engine)
session = Session()

for streamer_info in streamers_seed:
    streamer = StreamerModel()
    streamer.twitch_name = streamer_info['twitch_name']
    streamer.discord_id = streamer_info['discord_id']
    streamer.is_live = streamer_info['is_live']
    
    session.add(streamer)
session.commit()

for sub_info in subscribers_seed:
    subscriber = SubscriberModel()
    subscriber.phone_number = sub_info['phone_number']
    subscriber.discord_id = sub_info['discord_id']

    session.add(subscriber)
session.commit()
# ///////////////////////////////////
session.close()

print("no errors? noice")