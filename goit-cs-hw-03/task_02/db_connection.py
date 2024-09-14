import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, CollectionInvalid

load_dotenv()

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def connect(self):
        if self.client is not None:
            return  # Connection already established

        try:
            MONGO_URI = os.getenv("MONGO_URI")
            if not MONGO_URI:
                raise ConfigurationError("MONGO_URI is not set in the environment variables")
            
            self.client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
            self.client.admin.command('ping')  # Перевірка з'єднання
            self.db = self.client["cat_database"]
            print("Successfully connected to the database")
        except ConnectionFailure as e:
            print(f"Failed to connect to the database. Error: {e}")
            raise
        except ConfigurationError as e:
            print(f"Database configuration error: {e}")
            raise

    def get_collection(self, collection_name):
        try:
            if not self.db:
                self.connect()
            return self.db[collection_name]
        except ConnectionFailure as e:
            print(f"Помилка підключення до бази даних при отриманні колекції: {e}")
            raise
        except ConfigurationError as e:
            print(f"Помилка конфігурації при отриманні колекції: {e}")
            raise
        except CollectionInvalid as e:
            print(f"Помилка при отриманні колекції '{collection_name}': {e}")
            raise
        except Exception as e:
            print(f"Неочікувана помилка при отриманні колекції '{collection_name}': {e}")
            raise

    def close_connection(self):
        if self.client:
            self.client.close()
            print("Database connection closed")
            self.client = None
            self.db = None

# Створення глобального екземпляра для використання в інших модулях
db_connection = DatabaseConnection()