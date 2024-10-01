import logging
from pymongo.errors import ConfigurationError, ConnectionFailure
from db_connection import db_connection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CatOperations:
    def __init__(self):
        self.collection = None
        try:
            self.collection = db_connection.get_collection("cats")
        except (ConfigurationError, ConnectionFailure) as inner_e:
            logging.error("Помилка при ініціалізації CatOperations: %s", inner_e)

    def _ensure_connection(self):
        if self.collection is None:
            try:
                self.collection = db_connection.get_collection("cats")
            except (ConfigurationError, ConnectionFailure) as inner_e:
                logging.error("Помилка при спробі повторного підключення: %s", inner_e)
                raise

    def create_cat(self, name, age, features):
        self._ensure_connection()
        try:
            result = self.collection.insert_one({
                "name": name,
                "age": age,
                "features": features
            })
            return str(result.inserted_id)
        except Exception as inner_e:
            logging.error("Помилка при створенні кота: %s", inner_e)
            raise

    def get_all_cats(self):
        self._ensure_connection()
        try:
            return list(self.collection.find())
        except Exception as inner_e:
            logging.error("Помилка при отриманні всіх котів: %s", inner_e)
            raise

    def get_cat_by_name(self, name):
        self._ensure_connection()
        try:
            return self.collection.find_one({"name": name})
        except Exception as inner_e:
            logging.error("Помилка при пошуку кота за ім'ям: %s", inner_e)
            raise

    def update_cat_age(self, name, new_age):
        self._ensure_connection()
        try:
            result = self.collection.update_one(
                {"name": name},
                {"$set": {"age": new_age}}
            )
            
            if result.matched_count == 0:
                logging.info(f"Кота з ім'ям '{name}' не знайдено в базі даних.")
                return False
            elif result.matched_count == 1 and result.modified_count == 0:
                logging.info(f"Кота '{name}' знайдено, але вік не змінено. Можливо, вказаний вік вже встановлено.")
                return False
            elif result.matched_count == 1 and result.modified_count == 1:
                logging.info(f"Вік кота '{name}' успішно оновлено до {new_age}.")
                return True
            else:
                logging.info("Несподіваний результат оновлення.")
                
            logging.info("Детальна інформація про результат:")
            logging.info(f"Знайдено документів: {result.matched_count}")
            logging.info(f"Змінено документів: {result.modified_count}")
            logging.info(f"Підтверджено сервером: {result.acknowledged}")
            
            return result.modified_count > 0
        except Exception as inner_e:
            logging.error("Помилка при оновленні віку кота: %s", inner_e)
            raise

    def add_cat_feature(self, name, new_feature):
        self._ensure_connection()
        try:
            result = self.collection.update_one(
                {"name": name},
                {"$addToSet": {"features": new_feature}}
            )
            return result.modified_count > 0
        except Exception as inner_e:
            logging.error("Помилка при додаванні характеристики кота: %s", inner_e)
            raise

    def delete_cat(self, name):
        self._ensure_connection()
        try:
            result = self.collection.delete_one({"name": name})
            return result.deleted_count > 0
        except Exception as inner_e:
            logging.error("Помилка при видаленні кота: %s", inner_e)
            raise

try:
    cat_ops = CatOperations()
except (ConfigurationError, ConnectionFailure) as e:
    logging.error("Не вдалося створити екземпляр CatOperations: %s", e)
    cat_ops = None