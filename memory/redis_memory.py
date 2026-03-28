import json
import os

try:
    import redis
except ModuleNotFoundError:
    redis = None

### Connexion à redis
_redis_url = os.getenv("REDIS_URL")
if redis is not None:
    r = (
        redis.Redis.from_url(_redis_url, decode_responses=True)
        if _redis_url
        else redis.Redis(host="localhost", port=6379, decode_responses=True)
    )
else:
    r = None

_fallback_store_path = os.getenv(
    "IA_FALLBACK_HISTORY_FILE",
    os.path.join(os.path.dirname(__file__), "history_fallback.json"),
)


def _load_fallback_store():
    if not os.path.exists(_fallback_store_path):
        return {}

    try:
        with open(_fallback_store_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _persist_fallback_store(store):
    try:
        with open(_fallback_store_path, "w", encoding="utf-8") as file:
            json.dump(store, file)
    except Exception:
        pass


_fallback_store = _load_fallback_store()

def add_message(user_id , role , text):
    key = f"chat:{user_id}"
    try:
        if r is not None:
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
    _persist_fallback_store(_fallback_store)

def get_history(user_id):
    key = f"chat:{user_id}"
    try:
        if r is not None:
            history = r.get(key)
            history = json.loads(history) if history else []
            return history
    except Exception:
        pass

    return _fallback_store.get(key, [])