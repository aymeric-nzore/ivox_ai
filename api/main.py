from fastapi import FastAPI
from pydantic import BaseModel
from core.assistant import assistant_response

app = FastAPI()

class Request(BaseModel):
    user_id: str
    text: str


@app.get("/health")
def health():
    """Vérifie que l'API est en ligne."""
    return {"status": "ok"}

@app.post("/assistant")
def assistant(req: Request):
    """Endpoint principal pour Flutter"""
    response = assistant_response(req.user_id, req.text)
    return {"response": response}