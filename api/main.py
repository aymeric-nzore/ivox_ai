from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from core.assistant import assistant_response
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    user_id: str
    text: str

class LevelGenRequest(BaseModel):
    n: int = 5  # nombre de niveaux à générer

@app.get("/health")
def health():
    """Vérifie que l'API est en ligne."""
    return {"status": "ok"}

@app.post("/assistant")
def assistant(req: Request):
    """Endpoint principal pour Flutter"""
    response = assistant_response(req.user_id, req.text)
    return {"response": response}

# --- Génération et envoi de niveaux de mots croisés ---
@app.post("/generate-crosswords")
def generate_crosswords(req: LevelGenRequest):
    """Génère n niveaux de mots croisés et les envoie au backend."""
    backend_url = os.getenv("BACKEND_URL", "https://backend-q1iu.onrender.com")
    endpoint = f"{backend_url}/api/levels/save-words"
    results = []
    for i in range(1, req.n + 1):
        level = {
            "numero": i,
            "gridSize": {"rows": 8, "cols": 8},
            "timeLimit": 300 + i*30,
            "xpReward": 100 + i*10,
            "coinsReward": 10 + i*2,
            "words": [
                {"word": "CHAT", "row": 1, "col": 1, "direction": "accross"},
                {"word": "VOITURE", "row": 3, "col": 2, "direction": "down"},
                {"word": "SOLEIL", "row": 5, "col": 0, "direction": "accross"},
            ]
        }
        try:
            r = requests.post(endpoint, json=level, timeout=10)
            r.raise_for_status()
            results.append({"level": i, "status": "ok", "msg": r.json().get("message")})
        except Exception as e:
            results.append({"level": i, "status": "error", "msg": str(e)})
    return {"results": results}