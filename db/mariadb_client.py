import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "optimizer")
DB_PASSWORD = os.getenv("DB_PASS", "optimizer123")
DB_NAME = os.getenv("DB_NAME", "testdb")

def get_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"❌ Error connecting to MariaDB: {e}")
        return None

def execute_query(query):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        conn.close()
        return results
    except pymysql.MySQLError as e:
        print(f"❌ Error executing query: {e}")
        return None

def execute_explain(query):
    return execute_query(f"EXPLAIN {query}")
