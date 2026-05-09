# Database connection module for conference management system
# Author: Mariane McGrath

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Source: [https://pypi.org/project/python-dotenv/](PyPI Documentation)
# Source: [https://12factor.net/config](The Twelve-Factor App - Config)

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as e:
        print(f"*** ERROR *** {e}")
        return None