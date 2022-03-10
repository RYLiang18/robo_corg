from get_docker_secret import get_docker_secret

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_user = get_docker_secret('db_user')
db_pwd = get_docker_secret('db_pwd')

engine = create_engine(
    f'mysql+mysqlconnector://{db_user}:{db_pwd}@db/robocorg',
)

Session = sessionmaker(bind=engine)