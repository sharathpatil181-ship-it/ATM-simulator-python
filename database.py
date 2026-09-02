import mysql.connector
from mysql.connector.connection import MySQLConnection


def get_connection() -> MySQLConnection:
    return mysql.connector.connect(
        host="localhost",
        user="atmuser",
        password="atm123",
        database="atmdb"
    )
