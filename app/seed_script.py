from sqlalchemy import select

from database import Session
from database.models import (
    StreamerModel, SubscriberModel
)

from database.seed_data import (
    streamers_seed, subscribers_seed, relationship_seed
)

# overwrite db_init/init.sql since that doesn't have the phone_numbers
# column in subscribers table as bytes yet
# from database.models import base
# from database import engine

# base.metadata.drop_all(engine)
# base.metadata.create_all(bind=engine)

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
# for sub_info in subscribers_seed:
#     subscriber = SubscriberModel(
#         phone_number = sub_info['phone_number'],
#         discord_id = sub_info['discord_id']
#     )

#     session.add(subscriber)
# session.commit()

# populating RELATIONSHIP_TBL
# for relationship_info in relationship_seed:
#     select_streamer = select(StreamerModel).where(
#         StreamerModel.twitch_name == relationship_info['twitch_name']
#     )
#     streamer = session.execute(select_streamer).first().StreamerModel
#     # print(streamer.twitch_name)
    
#     select_subscriber = select(SubscriberModel).where(
#         SubscriberModel.phone_number == relationship_info['phone_number']
#     )
#     subscriber = session.execute(select_subscriber).first().SubscriberModel
#     # print(subscriber.phone_number)

#     streamer.subscribers.append(subscriber)
# session.commit()

# ///////////////////////////////////
session.close()

print("SEED DATA MIGRATED!")