from pymongo import MongoClient, ASCENDING, TEXT
from bson import ObjectId
import bcrypt
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

    def create_paper(self, paper_data, citations=None):
        paper_data['uploaded_by'] = ObjectId(paper_data['uploaded_by'])
        paper_data['views'] = 0
        result = self.papers.insert_one(paper_data)
        paper_id = result.inserted_id

        if citations:
            citation_docs = []
            for cited_id in citations:
                citation_docs.append({
                    "paper_id": paper_id,
                    "cited_paper_id": ObjectId(cited_id)
                })
            if citation_docs:
                self.citations.insert_many(citation_docs)

        return str(paper_id)

    def get_paper_by_id(self, paper_id):
        try:
            return self.papers.find_one({"_id": ObjectId(paper_id)})
        except:
            return None

    def search_papers(self, search_term="", sort_by="relevance", order="desc"):
        query = {}
        projection = None
        sort_direction = -1 if order == "desc" else 1

        # Set up text search if a search term is provided
        if search_term.strip():
            query["$text"] = {"$search": search_term}
            projection = {"score": {"$meta": "textScore"}}

        # Determine how to sort based on parameters and if text search is used
        if sort_by == "relevance" and search_term.strip():
            # Sort by text relevance score
            sort_spec = [("score", {"$meta": "textScore"})]
        else:
            # Sort by publication_date
            if search_term.strip():
                # When using text search but sorting by a field, include both
                sort_spec = [
                    ("publication_date", sort_direction),
                    ("score", {"$meta": "textScore"})
                ]
            else:
                # No text search, simple field sort
                sort_spec = [("publication_date", sort_direction)]

        # Execute the query with proper projection and sorting
        cursor = self.papers.find(query, projection)
        cursor = cursor.sort(sort_spec)

        return list(cursor)
