import mysql.connector
import os

def get_db_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD", ""),
        database="hospital_db"
    )

    return connection