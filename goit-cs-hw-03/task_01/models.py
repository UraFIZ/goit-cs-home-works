from database import execute_query
from psycopg2 import OperationalError

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER REFERENCES status(id),
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        )
        """)
    
    try:
        for command in commands:
            execute_query(command)
        logging.info("Tables created successfully")
    except OperationalError as e:
        logging.info(f"Error creating tables: {e}")
        raise

def insert_initial_statuses():
    query = "INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed') ON CONFLICT (name) DO NOTHING"
    try:
        execute_query(query)
        logging.info("Initial statuses inserted successfully")
    except OperationalError as e:
        logging.info(f"Error inserting initial statuses: {e}")
        raise

if __name__ == "__main__":
    try:
        create_tables()
        insert_initial_statuses()
    except OperationalError as e:
        logging.info(f"Database operation failed: {e}")