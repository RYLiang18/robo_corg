from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Table, LargeBinary
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

base = declarative_base()

association_table = Table(
    'RELATIONSHIP_TBL',
    base.metadata,
    Column(
        'streamer_id', Integer, ForeignKey('STREAMER_TBL.id'), primary_key=True
    ),
    Column(
        'subscriber_id', Integer, ForeignKey('SUBSCRIBER_TBL.id'), primary_key=True
    )
)

class StreamerModel(base):
    """
    SQLAlchemy Schema for the Streamer Table

    :id: <int> <primary key> Streamer ID in the database
    :twitch_name: <str> streamer's twitch name
    :is_live: <bool> 0 = offline, 1 = live
    :subscribers: <relationship> so each streamer can access their subscribers in SUBSCRIBER_TBL
    """
    __tablename__ = "STREAMER_TBL"
    id = Column(
        'id', Integer, primary_key=True
    )
    twitch_name = Column('twitch_name', String(100))
    is_live = Column('is_live', Boolean)

    subscribers = relationship(
        "SubscriberModel", secondary= association_table
    )

class SubscriberModel(base):
    """
    SQLAlchemy Schema for the Subscriber Table

    :id: <int> <primary key> subscriber's ID in the database
    :phone_number: <bytes> the subscriber's encrypted phone number
    :discord_id: <str> the subscriber's discord ID
    """
    __tablename__ = "SUBSCRIBER_TBL"
    id = Column(
        'id',
        Integer,
        primary_key=True
    )
    phone_number = Column('phone_number', LargeBinary(100))
    discord_id = Column('discord_id', String(100))