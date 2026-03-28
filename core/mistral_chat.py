import os
try:
    from mistralai import Mistral
except ImportError:
    from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def chat(messages):
    """Envoie toute la conversation à Mistral pour générer une réponse"""
    response = client.chat.complete(
        model="mistral-medium",
        messages=messages
    )
    return response.choices[0].message.content
