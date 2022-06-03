import os
# from get_docker_secret import get_docker_secret

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db_user = get_docker_secret('db_user')
# db_pwd = get_docker_secret('db_pwd')

parsed_db_url = os.environ.get("DATABASE_URL").partition("postgres://")[2]
sqlalchemy_conn_string = f"postgresql://{parsed_db_url}"
engine = create_engine(
    sqlalchemy_conn_string
)

Session = sessionmaker(bind=engine)