# Good Idea
# DIP = Dependency Inversion Principle

from abc import ABC, abstractmethod
class Database(ABC):
    @abstractmethod
    def save(self):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        print(f"Saving '{data}' to MySQL Database")

class PostgreSQLDatabase(Database):
    def save(self, data):
        print(f"Saving '{data}' to PostgreSQL Database")

class App:
    def __init__(self, db: Database):
        self.db = db

    def save_data(self, data):
        self.db.save(data)