from core.level_api import send_level_result
def process_level_end(user_id, score, time_seconds, level_num):
    """Appelle le backend pour ajouter XP, score et pièces à la fin d'un niveau."""
    result = send_level_result(user_id, score, time_seconds, level_num)
    if "error" in result:
        return f"Erreur lors de l'enregistrement du score: {result['error']}"
    msg = result.get("message", "")
    xp = result.get("xp", 0)
    coins = result.get("coins", 0)
    leveled_up = result.get("leveledUp", False)
    rep = f"{msg}\nTu gagnes {xp} XP et {coins} pièces."
    if leveled_up:
        rep += "\nBravo, tu passes au niveau supérieur !"
    return rep
from memory.redis_memory import add_message, get_history
from core.mistral_chat import chat
from core.translator import translate


def assistant_response(user_id, text):
    """Cœur de l'assistant"""
    try:
        # 1. Ajouter message utilisateur
        add_message(user_id, "user", text)

        # 2. Récupérer historique (limité pour accélérer la réponse)
        history = get_history(user_id)[-8:]

        # 3. Décider quoi faire
        if text.lower().startswith("traduire"):
            phrase = text.replace("traduire", "").strip()
            response = translate(phrase)
        else:
            response = chat(history)

        # 4. Ajouter réponse IA à l'historique
        add_message(user_id, "assistant", response)
        return response
    except Exception:
        return "Je suis Mylann. Je suis momentanement indisponible, reessaie dans quelques instants."