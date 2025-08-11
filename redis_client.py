import redis
import json
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_CACHE", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDID_DB = int(os.getenv("REDIS_DB", 0))


class RedisClient:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDID_DB):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.username_hash_key = "usernames"

    def is_username_taken(self, username: str) -> bool:
        return self.client.hexists(self.username_hash_key, username)

    def mark_username_taken(self, username: str) -> None:
        self.client.hset(self.username_hash_key, username, 1)

    def get_search_cache(self, search_term: str, sort_by: str, order: str) -> Optional[List[Dict[Any, Any]]]:
        cache_key = f"search:{search_term}:{sort_by}:{order}"
        cached_result = self.client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        return None

    def set_search_cache(self, search_term: str, sort_by: str, order: str,
                        results: List[Dict[Any, Any]], ttl: int = 300) -> None:
        cache_key = f"search:{search_term}:{sort_by}:{order}"
        self.client.setex(cache_key, ttl, json.dumps(results, default=str))

    def increment_paper_views(self, paper_id: str) -> int:
        view_key = f"paper_views:{paper_id}"
        return self.client.incr(view_key)

    def get_paper_views(self, paper_id: str) -> int:
        view_key = f"paper_views:{paper_id}"
        views = self.client.get(view_key)
        return int(views) if views else 0

    def get_all_paper_view_keys(self) -> List[str]:
        return self.client.keys("paper_views:*")

    def reset_paper_views(self, paper_id: str) -> None:
        view_key = f"paper_views:{paper_id}"
        self.client.set(view_key, 0)
