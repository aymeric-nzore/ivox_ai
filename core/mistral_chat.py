import os
try:
    from mistralai import Mistral
except ImportError:
    from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

def _build_client():
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return None
    try:
        return Mistral(api_key=api_key)
    except Exception:
        return None


client = _build_client()

def chat(messages):
    """Envoie toute la conversation à Mistral pour générer une réponse"""
    system_message = {
        "role": "system",
        "content": (
            "Tu es Mylann, la mascotte IA de l'application IVOX. "
            "Reponds en francais clair, chaleureux, concis, et bien structures. "
            "Utilise des retours a la ligne lisibles et evite les caracteres corrompus."
        ),
    }

    if client is None:
        return "Je suis Mylann. Je suis momentanement indisponible, reessaie dans quelques instants."

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[system_message, *messages],
        )
        return response.choices[0].message.content
    except Exception:
        return "Je suis Mylann. Je suis momentanement indisponible, reessaie dans quelques instants."
