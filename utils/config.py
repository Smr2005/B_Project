import pymysql
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# API keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Database settings from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")        # optimizer
DB_PASSWORD = os.getenv("DB_PASS")    # optimizer123
DB_NAME = os.getenv("DB_NAME", "test_db")  # replace with your DB name

# DB_CONFIG dictionary for existing imports
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "cursorclass": pymysql.cursors.Cursor
}

# Function to get a connection
def get_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.MySQLError as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

# Execute a normal query
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
        print(f"Error executing query: {e}")
        return None

# Execute EXPLAIN query
def execute_explain(query):
    return execute_query(f"EXPLAIN {query}")
