import signal
from cat_operations import cat_ops
from utils import logging.info_cat_info, get_user_input, exit_handler

def main():
    signal.signal(signal.SIGINT, exit_handler)
    try:
        while True:
            logging.info("\n1. Add a new cat")
            logging.info("2. View all cats")
            logging.info("3. Find a cat by name")
            logging.info("4. Update cat's age")
            logging.info("5. Add a feature to a cat")
            logging.info("6. Delete a cat")
            logging.info("7. Exit")

            choice = get_user_input("Enter your choice (1-7): ", int)

            if choice == 1:
                name = get_user_input("Enter cat's name: ")
                age = get_user_input("Enter cat's age: ", int)
                features = get_user_input("Enter cat's features (comma-separated): ").split(',')
                cat_id = cat_ops.create_cat(name, age, features)
                logging.info(f"Cat created with ID: {cat_id}")

            elif choice == 2:
                cats = cat_ops.get_all_cats()
                for cat in cats:
                    logging.info_cat_info(cat)

            elif choice == 3:
                name = get_user_input("Enter cat's name to find: ")
                cat = cat_ops.get_cat_by_name(name)
                logging.info_cat_info(cat)

            elif choice == 4:
                name = get_user_input("Enter cat's name to update: ")
                new_age = get_user_input("Enter new age: ", int)
                success = cat_ops.update_cat_age(name, new_age)
                logging.info("Age updated successfully" if success else "Failed to update age")

            elif choice == 5:
                name = get_user_input("Enter cat's name to update: ")
                new_feature = get_user_input("Enter new feature: ")
                success = cat_ops.add_cat_feature(name, new_feature)
                logging.info("Feature added successfully" if success else "Failed to add feature")

            elif choice == 6:
                name = get_user_input("Enter cat's name to delete: ")
                success = cat_ops.delete_cat(name)
                logging.info("Cat deleted successfully" if success else "Failed to delete cat")

            elif choice == 7:
                logging.info("Exiting program.")
                break

            else:
                logging.info("Invalid choice. Please try again.")

    except ValueError as e:
        logging.info(f"ValueError occurred: {e}")
    except KeyError as e:
        logging.info(f"KeyError occurred: {e}")
    finally:
        exit_handler()

if __name__ == "__main__":
    main()