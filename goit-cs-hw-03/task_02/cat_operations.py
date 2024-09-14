from db_connection import db_connection
from pymongo.errors import PyMongoError

class CatOperations:
    def __init__(self):
        self.collection = db_connection.get_collection("cats")

    def create_cat(self, name, age, features):
        try:
            result = self.collection.insert_one({
                "name": name,
                "age": age,
                "features": features
            })
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Error creating cat: {e}")
            return None

    def get_all_cats(self):
        try:
            return list(self.collection.find())
        except PyMongoError as e:
            print(f"Error retrieving cats: {e}")
            return []

    def get_cat_by_name(self, name):
        try:
            return self.collection.find_one({"name": name})
        except PyMongoError as e:
            print(f"Error retrieving cat by name: {e}")
            return None

    def update_cat_age(self, name, new_age):
        try:
            result = self.collection.update_one(
                {"name": name},
                {"$set": {"age": new_age}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating cat age: {e}")
            return False

    def add_cat_feature(self, name, new_feature):
        try:
            result = self.collection.update_one(
                {"name": name},
                {"$addToSet": {"features": new_feature}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            print(f"Error adding cat feature: {e}")
            return False

    def delete_cat(self, name):
        try:
            result = self.collection.delete_one({"name": name})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting cat: {e}")
            return False


cat_ops = CatOperations()
