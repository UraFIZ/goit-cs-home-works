import sys
from db_connection import db_connection


def logging.info_cat_info(cat):
    logging.info("\n" + "=" * 30) 
    if cat:
        logging.info(f"ID: {cat['_id']}")
        logging.info(f"Name: {cat['name']}")
        logging.info(f"Age: {cat['age']}")
        logging.info(f"Features: {', '.join(cat['features'])}")
        logging.info("-" * 30)
    else:
        logging.info("Cat not found")

def get_user_input(prompt, input_type=str):
    while True:
        try:
            user_input = input(prompt)
            return input_type(user_input)
        except ValueError:
            logging.info(f"Invalid input. Please enter a valid {input_type.__name__}")

def exit_handler():
    logging.info("\nДякуємо за використання програми Cat Database. До побачення!")
    db_connection.close_connection()
    sys.exit(0)
