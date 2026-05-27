from memory.redis_memory import add_message, get_history
from core.mistral_chat import chat
from core.translator import translate
import re


def _extract_translation_phrase(text: str):
    lowered = text.strip().lower()
    match = re.search(r"\b(?:traduit|traduire|traduis)\b", lowered)
    if not match:
        return None

    phrase = text[match.end():].strip()
    phrase = re.sub(r"\s+en\s+dioula\s*$", "", phrase, flags=re.IGNORECASE).strip(" ,.;:!?\"")
    return phrase


def assistant_response(user_id, text):
    """Cœur de l'assistant"""
    try:
        # 1. Ajouter message utilisateur
        add_message(user_id, "user", text)

        # 2. Récupérer historique (limité pour accélérer la réponse)
        history = get_history(user_id)[-8:]

        # 3. Décider quoi faire
        phrase = _extract_translation_phrase(text)
        if phrase is not None:
            if not phrase:
                response = "Donne-moi la phrase à traduire en dioula."
            else:
                response = translate(phrase)
        else:
            response = chat(history)

        # 4. Ajouter réponse IA à l'historique
        add_message(user_id, "assistant", response)
        return response
    except Exception:
        return "Je suis Mylann. Je suis momentanement indisponible, reessaie dans quelques instants."