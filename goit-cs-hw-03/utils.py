def format_tasks(tasks):
    formatted_output = ""
    for task in tasks:
        formatted_output += f"Task ID: {task[0]}\n"
        formatted_output += f"Title: {task[1]}\n"
        formatted_output += f"Description: {task[2][:50]}{'...' if len(task[2]) > 50 else ''}\n"
        formatted_output += f"Status ID: {task[3]}\n"
        formatted_output += f"User ID: {task[4]}\n"
        formatted_output += "-" * 50 + "\n"
    return formatted_output

def format_users(users):
    formatted_output = ""
    for user in users:
        formatted_output += f"User ID: {user[0]}\n"
        formatted_output += f"Full Name: {user[1]}\n"
        formatted_output += f"Email: {user[2]}\n"
        formatted_output += "-" * 50 + "\n"
    return formatted_output

def format_status_count(status_counts):
    formatted_output = "Task count by status:\n"
    for status in status_counts:
        formatted_output += f"{status[0]}: {status[1]}\n"
    return formatted_output

def format_user_task_count(user_task_counts):
    formatted_output = "Users and their task count:\n"
    for user_count in user_task_counts:
        formatted_output += f"{user_count[0]}: {user_count[1]} task(s)\n"
    return formatted_output

def format_user_tasks(user_tasks):
    formatted_output = "Users and their tasks:\n"
    for user_task in user_tasks:
        formatted_output += f"User: {user_task[0]}, Task: {user_task[1]}\n"
    return formatted_output

def format_query_result(result, query_type):
    if not result:
        return "No results found."
    
    if query_type == 'tasks':
        return format_tasks(result)
    elif query_type == 'users':
        return format_users(result)
    elif query_type == 'status_count':
        return format_status_count(result)
    elif query_type == 'user_task_count':
        return format_user_task_count(result)
    elif query_type == 'user_tasks':
        return format_user_tasks(result)
    else:
        return str(result)  # Повернення необробленого результату, якщо тип не визначено