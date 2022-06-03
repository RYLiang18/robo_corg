import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

parsed_db_url = os.environ.get("DATABASE_URL").partition("postgres://")[2]
sqlalchemy_conn_string = f"postgresql://{parsed_db_url}"
engine = create_engine(
    sqlalchemy_conn_string
)

Session = sessionmaker(bind=engine)