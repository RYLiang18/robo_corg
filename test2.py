# import mysql.connector
import os

from sqlalchemy import create_engine

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd = os.environ.get("mysql_root_pwd"),
#     database="linuxhint"
# )
db_pwd = os.environ.get("mysql_root_pwd")
engine = create_engine(f'mysql+mysqlconnector://root:{db_pwd}@localhost/robocorg')


print("no errors? noice")