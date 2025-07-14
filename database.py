from pymongo import MongoClient, ASCENDING, TEXT
from bson import ObjectId
import bcrypt
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 27017))
DB_NAME = os.getenv("DB_NAME", "research_papers")


class Database:
    def __init__(self, connection_string=f"mongodb://{DB_HOST}:{DB_PORT}/", db_name=DB_NAME):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.users = self.db.users
        self.papers = self.db.papers
        self.citations = self.db.citations
        self._create_indexes()

    def _create_indexes(self):
        try:
            self.users.create_index([("username", ASCENDING)], unique=True)

            self.papers.create_index([
                ("title", TEXT),
                ("abstract", TEXT),
                ("keywords", TEXT)
            ])

            self.citations.create_index([("cited_paper_id", ASCENDING)])

            print("Database indexes created successfully")
        except Exception as e:
            print(f"Error creating indexes: {e}")

    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def create_user(self, user_data):
        user_data['password'] = self._hash_password(user_data['password'])
        result = self.users.insert_one(user_data)
        return str(result.inserted_id)

    def get_user_by_username(self, username):
        return self.users.find_one({"username": username})

    def get_user_by_id(self, user_id):
        try:
            return self.users.find_one({"_id": ObjectId(user_id)})
        except:
            return None
