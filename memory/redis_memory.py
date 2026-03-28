import redis
import json
import os

### Connexion à redis
_redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(_redis_url, decode_responses=True) if _redis_url else redis.Redis(host="localhost", port=6379, decode_responses=True)
_fallback_store = {}

def add_message(user_id , role , text):
    key = f"chat:{user_id}"
    try:
        history = r.get(key)
        history = json.loads(history) if history else []

        history.append({"role" : role , "content" : text})
        r.set(key , json.dumps(history))
        return
    except Exception:
        # Fallback in-memory store to keep assistant available when Redis is down.
        pass

    history = _fallback_store.get(key, [])
    history.append({"role" : role , "content" : text})
    _fallback_store[key] = history

def get_history(user_id):
    key = f"chat:{user_id}"
    try:
        history = r.get(key)
        history = json.loads(history) if history else []
        return history
    except Exception:
        return _fallback_store.get(key, [])