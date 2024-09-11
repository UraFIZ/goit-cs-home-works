from models import create_tables, insert_initial_statuses
from seed import seed_data
from database import get_db_connection
from psycopg2 import OperationalError

def main():
    try:
        # Створення таблиць
        create_tables()
        insert_initial_statuses()
        
        # Заповнення тестовими даними
        seed_data()
        
        # Тестовий запит
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users LIMIT 5")
        users = cur.fetchall()
        cur.execute("SELECT * FROM tasks LIMIT 5")
        tasks = cur.fetchall()
        print("Sample users:")
        for user in users:
            print(user)
        
        cur.close()
        conn.close()
    except OperationalError as e:
        print(f"Error: {e}")
        # Optionally, you can log the error or take other actions here

if __name__ == "__main__":
    main()