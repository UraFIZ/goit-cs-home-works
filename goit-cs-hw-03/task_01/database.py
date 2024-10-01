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
            logging.info(f"Attempt {attempt + 1} of {retries} failed: {e}")
            attempt += 1
            time.sleep(delay)
    raise OperationalError(f"Could not connect to the database after {retries} attempts")


def execute_query(query, params=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                if cursor.description:
                    return cursor.fetchall()
    except OperationalError as e:
        logging.info(f"Database connection failed: {e}")
        raise e
    except Exception as e:
        logging.info(f"Error executing query: {e}")
        raise e
