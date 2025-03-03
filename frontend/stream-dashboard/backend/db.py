import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "streaming_analytics"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "..."),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )