import requests
import os

def send_level_result(user_id, score, time_seconds, level_num):
    """Envoie le résultat d'un niveau au backend pour ajouter XP, score et pièces."""
    backend_url = os.getenv("BACKEND_URL", "http://localhost:3000")
    url = f"{backend_url}/api/levels/add-xp-score"
    payload = {
        "userId": user_id,
        "score": score,
        "timeSeconds": time_seconds,
        "levelNumero": level_num
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
