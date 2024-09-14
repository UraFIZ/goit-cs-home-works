import sys
from db_connection import db_connection


def print_cat_info(cat):
    print("\n" + "=" * 30) 
    if cat:
        print(f"ID: {cat['_id']}")
        print(f"Name: {cat['name']}")
        print(f"Age: {cat['age']}")
        print(f"Features: {', '.join(cat['features'])}")
        print("-" * 30)
    else:
        print("Cat not found")

def get_user_input(prompt, input_type=str):
    while True:
        try:
            user_input = input(prompt)
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}")

def exit_handler():
    print("\nДякуємо за використання програми Cat Database. До побачення!")
    db_connection.close_connection()
    sys.exit(0)
