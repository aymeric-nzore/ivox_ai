import os
import requests
import random

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:3000")
LEVELS_ENDPOINT = f"{BACKEND_URL}/api/levels/save-words"

# Exemple de génération de 5 niveaux de mots croisés (à adapter selon ta logique IA)
def generate_crossword_levels(n=5):
    levels = []
    for i in range(1, n+1):
        level = {
            "numero": i,
            "gridSize": {"rows": 8, "cols": 8},
            "timeLimit": 300 + i*30,  # 5 à 7 min
            "xpReward": 100 + i*10,
            "coinsReward": 10 + i*2,
            "words": [
                {"word": "CHAT", "row": 1, "col": 1, "direction": "accross"},
                {"word": "VOITURE", "row": 3, "col": 2, "direction": "down"},
                {"word": "SOLEIL", "row": 5, "col": 0, "direction": "accross"},
            ]
        }
        levels.append(level)
    return levels

def send_level_to_backend(level):
    try:
        r = requests.post(LEVELS_ENDPOINT, json=level, timeout=10)
        r.raise_for_status()
        print(f"Niveau {level['numero']} envoyé: {r.json().get('message')}")
    except Exception as e:
        print(f"Erreur en envoyant le niveau {level['numero']}: {e}")

if __name__ == "__main__":
    levels = generate_crossword_levels(5)
    for level in levels:
        send_level_to_backend(level)
