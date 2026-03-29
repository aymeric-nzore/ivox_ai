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

@app.get("/health")
def health():
    """Vérifie que l'API est en ligne."""
    return {"status": "ok"}

@app.post("/assistant")
def assistant(req: Request):
    """Endpoint principal pour Flutter"""
    response = assistant_response(req.user_id, req.text)
    return {"response": response}