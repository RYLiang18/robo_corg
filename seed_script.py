from sqlalchemy import select

from database import Session
from database.models import (
    base, StreamerModel, SubscriberModel
)

from database.seed_data import (
    streamers_seed, subscribers_seed, relationship_seed
)

# overwrite db_init/init.sql since that doesn't have the phone_numbers
# column in subscribers table as bytes yet
from database.models import base
from database import engine

base.metadata.drop_all(engine)
base.metadata.create_all(bind=engine)

with Session() as session:
    # checking if tables are empty
    if session.query(StreamerModel).first() is None:
        # populating STREAMER_TBL
        for streamer_info in streamers_seed:
            streamer = StreamerModel(
                twitch_name = streamer_info['twitch_name'],
                is_live = streamer_info['is_live']
            )
            
            session.add(streamer)
        session.commit()

print("SEED DATA MIGRATED!")