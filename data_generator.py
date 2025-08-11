from faker import Faker
from database import Database
from redis_client import RedisClient
import random
from datetime import datetime, date
from bson import ObjectId

fake = Faker(['en_US'])


class DataGenerator:
    def __init__(self):
        self.db = Database()
        self.redis_client = RedisClient()

    def generate_users(self, count=100):
        print(f"{count} users are being generated...")

        usernames = set()
        users_data = []

        for i in range(count):
            # Generate a unique username
            while True:
                username = fake.user_name()[:20]
                if username not in usernames and not self.redis_client.is_username_taken(username):
                    usernames.add(username)
                    break

            # Generate other user data
            user_data = {
                'username': username,
                'name': fake.name()[:100],
                'email': fake.email()[:100],
                'password': fake.password(length=random.randint(8, 12)),
                'department': fake.company()[:100]
            }

            try:
                user_id = self.db.create_user(user_data)
                users_data.append({
                    'id': user_id,
                    'username': username
                })

                # Mark the username as taken in Redis
                self.redis_client.mark_username_taken(username)

            except Exception as e:
                print(f"Error creating user {i}: {username}: {e}")
                continue

        print(f"Generated {len(users_data)} users successfully")
        return users_data

    def generate_papers(self, users_data, count=1000):
        print(f"{count} papers are being generated...")

        papers_data = []
        for i in range(count):
            try:
                paper_data = {
                    'uploaded_by': random.choice(users_data)['id'],
                    'title': fake.sentence(nb_words=random.randint(6, 10))[:200],
                    'authors': [fake.name()[:100] for _ in range(random.randint(1, 5))],
                    'publication_date': fake.date_between(start_date=date(2015, 1, 1), end_date=datetime.now()).isoformat(),
                    'abstract': fake.paragraph(nb_sentences=random.randint(3, 8))[:1000],
                    'journal_conference': fake.company()[:200],
                    'keywords': [fake.word()[:50] for _ in range(random.randint(1, 5))]
                }

                paper_id = self.db.create_paper(paper_data)
                papers_data.append({
                    'id': paper_id,
                    'title': paper_data['title']
                })

            except Exception as e:
                print(f"Error creating paper {i}: {e}")
                continue

        print(f"Generated {len(papers_data)} papers successfully")
        return papers_data

    def generate_citations(self, papers_data):
        print("Generating citations...")

        citations_count = 0

        for paper in papers_data:
            try:
                num_citations = random.randint(0, 5)

                if num_citations > 0:
                    # Choose random papers to cite, excluding the current paper
                    available_papers = papers_data.copy()
                    available_papers.remove(paper)

                    if len(available_papers) >= num_citations:
                        cited_papers = random.sample(available_papers, num_citations)

                        citation_docs = []
                        for cited_paper in cited_papers:
                            citation_docs.append({
                                "paper_id": ObjectId(paper['id']),
                                "cited_paper_id": ObjectId(cited_paper['id'])
                            })

                        if citation_docs:
                            self.db.citations.insert_many(citation_docs)
                            citations_count += len(citation_docs)

            except Exception as e:
                print(f"Error creating citations for paper {paper['title']}: {e}")
                continue

        print(f"Generated {citations_count} citations successfully")

    def generate_all_data(self):
        print("Starting to generate test data...")

        # self.db.users.delete_many({})
        # self.db.papers.delete_many({})
        # self.db.citations.delete_many({})
        # self.redis_client.client.delete("usernames")

        users_data = self.generate_users(100)
        papers_data = self.generate_papers(users_data, 1000)
        self.generate_citations(papers_data)

        print("Data generation completed successfully!")
        print(f"Final counts:")
        print(f"Users: {self.db.users.count_documents({})}")
        print(f"Papers: {self.db.papers.count_documents({})}")
        print(f"Citations: {self.db.citations.count_documents({})}")


if __name__ == '__main__':
    generator = DataGenerator()
    generator.generate_all_data()
