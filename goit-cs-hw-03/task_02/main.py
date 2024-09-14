import signal
from cat_operations import cat_ops
from utils import print_cat_info, get_user_input, exit_handler

def main():
    signal.signal(signal.SIGINT, exit_handler)
    try:
        while True:
            print("\n1. Add a new cat")
            print("2. View all cats")
            print("3. Find a cat by name")
            print("4. Update cat's age")
            print("5. Add a feature to a cat")
            print("6. Delete a cat")
            print("7. Exit")

            choice = get_user_input("Enter your choice (1-7): ", int)

            if choice == 1:
                name = get_user_input("Enter cat's name: ")
                age = get_user_input("Enter cat's age: ", int)
                features = get_user_input("Enter cat's features (comma-separated): ").split(',')
                cat_id = cat_ops.create_cat(name, age, features)
                print(f"Cat created with ID: {cat_id}")

            elif choice == 2:
                cats = cat_ops.get_all_cats()
                for cat in cats:
                    print_cat_info(cat)

            elif choice == 3:
                name = get_user_input("Enter cat's name to find: ")
                cat = cat_ops.get_cat_by_name(name)
                print_cat_info(cat)

            elif choice == 4:
                name = get_user_input("Enter cat's name to update: ")
                new_age = get_user_input("Enter new age: ", int)
                success = cat_ops.update_cat_age(name, new_age)
                print("Age updated successfully" if success else "Failed to update age")

            elif choice == 5:
                name = get_user_input("Enter cat's name to update: ")
                new_feature = get_user_input("Enter new feature: ")
                success = cat_ops.add_cat_feature(name, new_feature)
                print("Feature added successfully" if success else "Failed to add feature")

            elif choice == 6:
                name = get_user_input("Enter cat's name to delete: ")
                success = cat_ops.delete_cat(name)
                print("Cat deleted successfully" if success else "Failed to delete cat")

            elif choice == 7:
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please try again.")

    except ValueError as e:
        print(f"ValueError occurred: {e}")
    except KeyError as e:
        print(f"KeyError occurred: {e}")
    finally:
        exit_handler()

if __name__ == "__main__":
    main()