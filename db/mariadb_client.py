# db/mariadb_client.py
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "optimizer")
DB_PASSWORD = os.getenv("DB_PASS", "optimizer123")
DB_NAME = os.getenv("DB_NAME", "testdb")  # your DB name

def get_connection():
    """
    Create and return a MariaDB connection.
    """
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=DictCursor   # Use DictCursor for easier row access
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def execute_query(query):
    """
    Execute a SQL query and return results.
    """
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
        print(f"Error executing query: {e}")
        return None

def execute_explain(query):
    """
    Execute EXPLAIN on a query for optimization hints.
    """
    return execute_query(f"EXPLAIN {query}")
