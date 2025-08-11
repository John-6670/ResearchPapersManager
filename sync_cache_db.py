from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from database import Database
from redis_client import RedisClient


class ViewSyncTask:
    def __init__(self):
        self.db = Database()
        self.redis_client = RedisClient()
        self.scheduler = BackgroundScheduler()

    def sync_views_from_redis_to_mongodb(self):
        try:
            print("Starting synchronization of paper views from Redis to MongoDB...")

            view_keys = self.redis_client.get_all_paper_view_keys()

            synced_count = 0
            for key in view_keys:
                try:
                    # Get paper ID from the Redis key
                    paper_id = key.split(':')[1]

                    view_count = self.redis_client.get_paper_views(paper_id)

                    if view_count > 0:
                        if self.db.update_paper_views(paper_id, view_count):
                            self.redis_client.reset_paper_views(paper_id)
                            synced_count += 1

                except Exception as e:
                    print(f"Error processing key {key}: {e}")
                    continue

            print(f"Synchronization complete. Synced {synced_count} paper views to MongoDB.")

        except Exception as e:
            print(f"Error while syncing: {e}")

    def start_scheduler(self):
        self.scheduler.add_job(
            func=self.sync_views_from_redis_to_mongodb,
            trigger="interval",
            minutes=10,
            id='sync_views',
            name='Sync paper views from Redis to MongoDB'
        )

        self.scheduler.start()
        print("Background scheduler started for syncing views.")

        # Register shutdown function to stop the scheduler on exit
        atexit.register(lambda: self.scheduler.shutdown())


def start_background_tasks():
    sync_task = ViewSyncTask()
    sync_task.start_scheduler()
    return sync_task


if __name__ == '__main__':
    sync_task = ViewSyncTask()
    sync_task.sync_views_from_redis_to_mongodb()
