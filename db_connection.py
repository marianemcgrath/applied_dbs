# db_connection.py

import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='appdbproj',
            port=3306,        
        )
        return conn
    
    except mysql.connector.Error as e:
        print(f"*** ERROR *** {e}")
        return None
    
# Note: Credentials are for default WAMP setup (no password)
# For other environments, modify the connection parameters below