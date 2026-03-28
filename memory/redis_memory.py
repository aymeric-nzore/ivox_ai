import redis
import json
import os

### Connexion à redis
r = redis.Redis(os.getenv("REDIS_URL"), decode_responses=True)

def add_message(user_id , role , text):
    key = f"chat:{user_id}"
    history = r.get(key)
    history = json.loads(history) if history else []

    history.append({"role" : role , "content" : text})
    r.set(key , json.dumps(history))

def get_history(user_id):
    key = f"chat:{user_id}"
    history = r.get(key)
    history = json.loads(history) if history else []
    return history