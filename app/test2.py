from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from get_docker_secret import get_docker_secret
# import os

db_user = get_docker_secret('db_user')
db_pwd = get_docker_secret('db_pwd')

print(db_user)
print(db_pwd)

engine = create_engine(
    f'mysql+mysqlconnector://{db_user}:{db_pwd}@db/robocorg',
    pool_pre_ping=True
)

conn = engine.connect()
conn.close()

# Session = sessionmaker(bind=engine)
# session = Session()

print("SUCCESS!!!!!")