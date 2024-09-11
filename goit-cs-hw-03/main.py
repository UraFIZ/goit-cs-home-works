from models import create_tables, insert_initial_statuses
from seed import seed_data
from database import execute_query
from psycopg2 import OperationalError

def main():
    try:
        # Створення таблиць
        create_tables()
        insert_initial_statuses()
        
        # Заповнення тестовими даними
        seed_data()
        
        # Виведення всіх користувачів
        users = execute_query("SELECT * FROM users LIMIT 5")
        if users is not None:
            print("All users:")
            for user in users:
                print(user)
        else:
            print("Failed to retrieve users")

        # Виведення всіх завдань
        tasks = execute_query("SELECT * FROM tasks LIMIT 5")
        if tasks is not None:
            print("\nAll tasks:")
            for task in tasks:
                print(task)
        else:
            print("Failed to retrieve tasks")

    except OperationalError as e:
        print(f"Fatal error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()