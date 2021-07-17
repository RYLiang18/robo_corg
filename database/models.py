from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey

base = declarative_base()

class StreamerModel(base):
    __tablename__ = "STREAMER_TBL"
    id = Column(
        'id', Integer, primary_key=True
    )
    twitch_name = Column('twitch_name', String(100))
    discord_id = Column('discord_id', String(100))
    is_live = Column('is_live', Boolean)

class SubscriberModel(base):
    __tablename__ = "SUBSCRIBER_TBL"
    id = Column(
        'id',
        Integer,
        primary_key=True
    )
    phone_number = Column('phone_number', String(100))
    discord_id = Column('discord_id', String(100))

class RelationshipModel(base):
    __tablename__ = "RELATIONSHIP_TBL"
    streamer_id = Column(
        'streamer_id', ForeignKey('STREAMER_TBL.id'), primary_key=True
    )
    subscriber_id = Column(
        'subscriber_id', ForeignKey('SUBSCRIBER_TBL.id'), primary_key=True
    )
