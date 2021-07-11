# import mysql.connector
import os
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



print("no errors? noice")