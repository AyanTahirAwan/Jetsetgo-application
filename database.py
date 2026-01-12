import mysql.connector 
from mysql.connector import Error


conn={
    "host":"localhost",
    "user":"jetsetgo",
    "password":"22247076",
    "database": "aviation_cli",
    "port": 3306
    }
db= mysql.connector.connect(**conn)
cursor=db.cursor()

