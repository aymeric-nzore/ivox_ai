import os
import re
try:
    from mistralai import Mistral
except ImportError:
    try:
        from mistralai.client import Mistral
    except ImportError:
        Mistral = None

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        return False

load_dotenv()

def _build_client():
    if Mistral is None:
        return None

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return None
    try:
        return Mistral(api_key=api_key)
    except Exception:
        return None


client = _build_client()


def _sanitize_reply(text):
    """Nettoie le markdown excessif: pas de titres/listes, gras autorise."""
    if not text:
        return ""

    cleaned = text.replace("\r\n", "\n")

    # Supprime les titres markdown (### Titre -> Titre)
    cleaned = re.sub(r"(?m)^\s*#{1,6}\s*", "", cleaned)

    # Supprime les puces markdown classiques en debut de ligne
    cleaned = re.sub(r"(?m)^\s*[-*]\s+", "", cleaned)

    # Supprime les etoiles seules utilisees comme decoration
    cleaned = cleaned.replace("***", "")

    # Garde le gras **mot**, mais retire les etoiles isolees restantes
    cleaned = re.sub(r"(?<!\*)\*(?!\*)", "", cleaned)

    # Limite les lignes vides consecutives
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()

def chat(messages):
    """Envoie toute la conversation à Mistral pour générer une réponse"""
    system_message = {
        "role": "system",
        "content": (
            "Tu es Mylann, la mascotte IA de l'application IVOX. "
            "Tu reponds en francais simple, naturel et chaleureux. "
            "N'utilise pas de titres markdown, pas de listes avec #, *, -, ni de mise en forme excessive. "
            "Tu peux uniquement utiliser le gras **comme ceci** pour 1 a 3 mots vraiment importants. "
            "Quand on te demande ton createur, tu reponds que ton createur est Aymeric. "
            "Quand on te demande l'origine de ton nom, tu dis que le nom Mylann est en l'honneur de la soeur d'Aymeric, "
            "qui est partie au Bresil pour des études en Architecture et qui s'appelle Mylann. "
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
        content = response.choices[0].message.content
        return _sanitize_reply(content)
    except Exception:
        return "Je suis Mylann. Je suis momentanement indisponible, reessaie dans quelques instants."
