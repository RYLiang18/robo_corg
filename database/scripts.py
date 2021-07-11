# import mysql.connector
import os

from twitchAPI.twitch import Twitch
from twitch_aux import Twitch_Aux
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

from models import (
    base, StreamerModel, SubscriberModel, RelationshipModel
)

# connecting the database
db_pwd = os.environ.get("mysql_root_pwd")
engine = create_engine(f'mysql+mysqlconnector://root:{db_pwd}@localhost/robocorg')

# create tables based on the models, i guess
base.metadata.create_all(bind=engine)

# ///////////////////////////////////
Session = sessionmaker(bind=engine)
session = Session()

# ///////////////////////////////////


print("no errors? noice")