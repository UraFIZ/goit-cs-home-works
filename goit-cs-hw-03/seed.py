from database import get_db_connection
import random
from faker import Faker
from psycopg2 import OperationalError, DatabaseError

fake = Faker()

def seed_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return

    try:
        # Додавання користувачів
        for _ in range(10):
            fullname = fake.name()
            email = fake.email()
            try:
                cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
            except DatabaseError as e:
                print(f"Error inserting user {fullname}: {e}")
                conn.rollback()
                continue

        # Отримання id всіх користувачів та статусів
        try:
            cur.execute("SELECT id FROM users")
            user_ids = [row[0] for row in cur.fetchall()]
        except DatabaseError as e:
            print(f"Error fetching user IDs: {e}")
            conn.rollback()
            return

        try:
            cur.execute("SELECT id FROM status")
            status_ids = [row[0] for row in cur.fetchall()]
        except DatabaseError as e:
            print(f"Error fetching status IDs: {e}")
            conn.rollback()
            return

        # Додавання завдань
        for _ in range(20):
            title = fake.sentence()
            description = fake.text()
            status_id = random.choice(status_ids)
            user_id = random.choice(user_ids)
            try:
                cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                            (title, description, status_id, user_id))
            except DatabaseError as e:
                print(f"Error inserting task {title}: {e}")
                conn.rollback()
                continue

        conn.commit()
    except Exception as e:
        print(f"Unexpected error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()