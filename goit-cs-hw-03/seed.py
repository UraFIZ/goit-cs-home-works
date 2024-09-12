from faker import Faker
from database import execute_query
import random

fake = Faker()

def seed_data():
    # Перевірка наявності даних
    existing_users = execute_query("SELECT COUNT(*) FROM users")
    if existing_users and existing_users[0][0] > 0:
        print("Data already exists. Skipping seed process.")
        return

    try:
        # Додавання користувачів
        for _ in range(10):
            fullname = fake.name()
            email = fake.email()
            execute_query("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

        # Отримання id всіх користувачів та статусів
        user_ids = execute_query("SELECT id FROM users")
        status_ids = execute_query("SELECT id FROM status")

        if not user_ids or not status_ids:
            raise ValueError("Failed to retrieve user or status ids")

        user_ids = [row[0] for row in user_ids]
        status_ids = [row[0] for row in status_ids]

        # Додавання завдань
        for _ in range(20):
            title = fake.sentence()
            description = fake.text()
            status_id = random.choice(status_ids)
            user_id = random.choice(user_ids)
            execute_query("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                          (title, description, status_id, user_id))

        print("Database seeded successfully")
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise