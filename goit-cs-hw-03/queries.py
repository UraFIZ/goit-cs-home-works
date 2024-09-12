from database import execute_query

def get_all_users():
    query = """
    SELECT * FROM users
    """
    return execute_query(query)

# 1. Отримати всі завдання певного користувача
def get_user_tasks(user_id):
    query = """
    SELECT * FROM tasks WHERE user_id = %s
    """
    return execute_query(query, (user_id,))

def get_user_tasks_by_title(user_id, title):
    query = """
    SELECT * FROM tasks WHERE user_id = %s AND title = %s
    """
    return execute_query(query, (user_id, title))

# 2. Вибрати завдання за певним статусом
def get_tasks_by_status(status_name):
    query = """
    SELECT * FROM tasks 
    WHERE status_id = (SELECT id FROM status WHERE name = %s)
    """
    return execute_query(query, (status_name,))

# 3.0 Знайти конкретне завдання
def get_task(task_id):
    query = """
    SELECT * FROM tasks WHERE id = %s
    """
    return execute_query(query, (task_id,))

# 3. Оновити статус конкретного завдання
def update_task_status(task_id, new_status):
    query = """
    UPDATE tasks 
    SET status_id = (SELECT id FROM status WHERE name = %s)
    WHERE id = %s
    """
    return execute_query(query, (new_status, task_id))

# 4. Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    query = """
    SELECT * FROM users 
    WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)
    """
    return execute_query(query)

# 5. Додати нове завдання для конкретного користувача
def add_new_task(title, description, status_id, user_id):
    query = """
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (title, description, status_id, user_id))

# 6. Отримати всі завдання, які ще не завершено
def get_uncompleted_tasks():
    query = """
    SELECT * FROM tasks 
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """
    return execute_query(query)

# 7. Видалити конкретне завдання
def delete_task(task_id):
    query = """
    DELETE FROM tasks WHERE id = %s
    """
    return execute_query(query, (task_id,))

# 8. Знайти користувачів з певною електронною поштою
def find_users_by_email(email_pattern):
    query = """
    SELECT * FROM users WHERE email LIKE %s
    """
    return execute_query(query, (f'%{email_pattern}%',))

# 9. Оновити ім'я користувача
def update_user_name(user_id, new_name):
    query = """
    UPDATE users SET fullname = %s WHERE id = %s
    """
    return execute_query(query, (new_name, user_id))

# 10. Отримати кількість завдань для кожного статусу
def get_task_count_by_status():
    query = """
    SELECT s.name, COUNT(t.id) 
    FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name
    """
    return execute_query(query)

# 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_user_email_domain(domain):
    query = """
    SELECT t.* 
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE %s
    """
    return execute_query(query, (f'%@{domain}',))

# 12. Отримати список завдань, що не мають опису
def get_tasks_without_description():
    query = """
    SELECT * FROM tasks WHERE description IS NULL OR description = ''
    """
    return execute_query(query)

# 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_with_in_progress_tasks():
    query = """
    SELECT u.fullname, t.title
    FROM users u
    JOIN tasks t ON u.id = t.user_id
    JOIN status s ON t.status_id = s.id
    WHERE s.name = 'in progress'
    """
    return execute_query(query)

# 14. Отримати користувачів та кількість їхніх завдань
def get_users_task_count():
    query = """
    SELECT u.fullname, COUNT(t.id) as task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id, u.fullname
    """
    return execute_query(query)

