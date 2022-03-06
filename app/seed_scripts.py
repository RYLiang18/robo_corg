# import mysql.connector
import os
from get_docker_secret import get_docker_secret

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from database.models import (
    base, StreamerModel, SubscriberModel
)

from seed_data import (
    streamers_seed, subscribers_seed, relationship_seed
)

# connecting the database
db_user = get_docker_secret('db_user')
db_pwd = get_docker_secret('db_pwd')

engine = create_engine(
    f'mysql+mysqlconnector://{db_user}:{db_pwd}@db/robocorg',
)

# wipe the database and create tables from scratch
# have a feeling this is terrible practice
# base.metadata.drop_all(engine)
# base.metadata.create_all(bind=engine)

# ///////////////////////////////////
Session = sessionmaker(bind=engine)
session = Session()

# populating STREAMER_TBL
for streamer_info in streamers_seed:
    streamer = StreamerModel(
        twitch_name = streamer_info['twitch_name'],
        is_live = streamer_info['is_live']
    )
    
    session.add(streamer)
session.commit()

# populating SUBSCRIBER_TBL
for sub_info in subscribers_seed:
    subscriber = SubscriberModel(
        phone_number = sub_info['phone_number'],
        discord_id = sub_info['discord_id']
    )

    session.add(subscriber)
session.commit()

# populating RELATIONSHIP_TBL
for relationship_info in relationship_seed:
    select_streamer = select(StreamerModel).where(
        StreamerModel.twitch_name == relationship_info['twitch_name']
    )
    streamer = session.execute(select_streamer).first().StreamerModel
    # print(streamer.twitch_name)
    
    select_subscriber = select(SubscriberModel).where(
        SubscriberModel.phone_number == relationship_info['phone_number']
    )
    subscriber = session.execute(select_subscriber).first().SubscriberModel
    # print(subscriber.phone_number)

    streamer.subscribers.append(subscriber)
session.commit()

# ///////////////////////////////////
session.close()

print("no errors? noice")