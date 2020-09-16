import mysql.connector
from libraries.constants import SETTINGS

HOSTNAME = SETTINGS["database"]["hostname"]
USERNAME = SETTINGS["database"]["username"]
PASSWORD = SETTINGS["database"]["password"]
DATABASE = SETTINGS["database"]["database"]

settings = {
    "host":HOSTNAME,
    "user":USERNAME,
    "password":PASSWORD,
    "database":DATABASE
}

class DB():
    def __init__(self):
        self.connection = mysql.connector.connect(**settings)

    def __del__(self):
        self.connection.close()


    
