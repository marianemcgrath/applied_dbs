# Connecting the database with Python

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="appdbproj"
    )