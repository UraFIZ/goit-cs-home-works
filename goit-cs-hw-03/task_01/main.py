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

        logging.info("Tasks for user with id 1:")
        logging.info(format_query_result(get_user_tasks(1), 'tasks'))

        logging.info("\nTasks with 'new' status:")
        logging.info(format_query_result(get_tasks_by_status('new'), 'tasks'))

        logging.info("\nUpdating task 1 status to 'in progress':")
        update_task_status(1, 'in progress')

        logging.info("\nUsers without tasks:")
        logging.info(format_query_result(get_users_without_tasks(), 'users'))

        logging.info("\nAdding new task:")
        add_new_task("New task", "Description", 1, 1)

        logging.info("\nUncompleted tasks:")
        logging.info(format_query_result(get_uncompleted_tasks(), 'tasks'))

        logging.info("\nDeleting task 1:")
        delete_task(1)

        logging.info("\nUsers with email containing 'example':")
        logging.info(format_query_result(find_users_by_email('example'), 'users'))

        logging.info("\nUpdating user 1 name:")
        update_user_name(1, "New Name")

        logging.info("\nTask count by status:")
        logging.info(format_query_result(get_task_count_by_status(), 'status_count'))

        logging.info("\nTasks for users with email domain 'example.com':")
        logging.info(format_query_result(get_tasks_by_user_email_domain('example.com'), 'tasks'))

        logging.info("\nTasks without description:")
        logging.info(format_query_result(get_tasks_without_description(), 'tasks'))

        logging.info("\nUsers with in-progress tasks:")
        logging.info(format_query_result(get_users_with_in_progress_tasks(), 'user_tasks'))

        logging.info("\nUsers and their task count:")
        logging.info(format_query_result(get_users_task_count(), 'user_task_count'))

    except OperationalError as e:
        logging.info(f"Fatal error: {e}")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
