import mysql.connector
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd = os.environ.get("mysql_root_pwd"),
    database="linuxhint"
)

print("no errors? noice")