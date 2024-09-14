from models import create_tables, insert_initial_statuses
from seed import seed_data
from psycopg2 import OperationalError
from queries import (
    get_tasks_by_status,
    update_task_status,
    get_users_without_tasks,
    add_new_task,
    get_user_tasks,
    get_uncompleted_tasks,
    delete_task,
    find_users_by_email,
    update_user_name,
    get_task_count_by_status,
    get_tasks_by_user_email_domain,
    get_tasks_without_description,
    get_users_with_in_progress_tasks,
    get_users_task_count
)
from utils import format_query_result


def main():
    try:
        # Створення таблиць
        create_tables()
        insert_initial_statuses()

        # Заповнення тестовими даними
        seed_data()

        print("Tasks for user with id 1:")
        print(format_query_result(get_user_tasks(1), 'tasks'))

        print("\nTasks with 'new' status:")
        print(format_query_result(get_tasks_by_status('new'), 'tasks'))

        print("\nUpdating task 1 status to 'in progress':")
        update_task_status(1, 'in progress')

        print("\nUsers without tasks:")
        print(format_query_result(get_users_without_tasks(), 'users'))

        print("\nAdding new task:")
        add_new_task("New task", "Description", 1, 1)

        print("\nUncompleted tasks:")
        print(format_query_result(get_uncompleted_tasks(), 'tasks'))

        print("\nDeleting task 1:")
        delete_task(1)

        print("\nUsers with email containing 'example':")
        print(format_query_result(find_users_by_email('example'), 'users'))

        print("\nUpdating user 1 name:")
        update_user_name(1, "New Name")

        print("\nTask count by status:")
        print(format_query_result(get_task_count_by_status(), 'status_count'))

        print("\nTasks for users with email domain 'example.com':")
        print(format_query_result(get_tasks_by_user_email_domain('example.com'), 'tasks'))

        print("\nTasks without description:")
        print(format_query_result(get_tasks_without_description(), 'tasks'))

        print("\nUsers with in-progress tasks:")
        print(format_query_result(get_users_with_in_progress_tasks(), 'user_tasks'))

        print("\nUsers and their task count:")
        print(format_query_result(get_users_task_count(), 'user_task_count'))

    except OperationalError as e:
        print(f"Fatal error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
