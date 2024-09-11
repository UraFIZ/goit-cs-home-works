import os
import time
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

def get_db_connection(retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            return conn
        except OperationalError as e:
            print(f"Attempt {attempt + 1} of {retries} failed: {e}")
            attempt += 1
            time.sleep(delay)
    raise OperationalError(f"Could not connect to the database after {retries} attempts")