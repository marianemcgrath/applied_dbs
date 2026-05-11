import mysql.connector

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="appdbproj"
    )
    print("✅ Direct MySQL connection successful!")
    conn.close()
except mysql.connector.Error as e:
    print(f"❌ MySQL error: {e}")