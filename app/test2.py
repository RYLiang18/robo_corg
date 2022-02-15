from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import os

db_user = os.environ.get("DB_USER")
db_pwd = os.environ.get("DB_PWD")

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