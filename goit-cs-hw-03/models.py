from database import get_db_connection

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
    
    conn = get_db_connection()
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()
    conn.close()

def insert_initial_statuses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed') ON CONFLICT (name) DO NOTHING")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
    insert_initial_statuses()
    print("Tables created successfully")