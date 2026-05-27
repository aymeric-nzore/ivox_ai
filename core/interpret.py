import os
import json

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()

OpenAI = None
_client = None


def _load_openai_client():
    global OpenAI, _client

    if _client is not None:
        return _client

    if OpenAI is None:
        try:
            from openai import OpenAI as openai_class
        except ImportError:
            return None
        OpenAI = openai_class

    api_key = os.getenv("OPEN_AI_API_KEY")
    if not api_key:
        return None

    try:
        _client = OpenAI(api_key=api_key)
    except Exception:
        _client = None

    return _client

def interpret_command(text : str):
    """Transforme un texte utilisateur en action JSON exploitable par une application mobile"""
    prompt = f"""
    Tu es une IA qui transforme une phrase de l'utilisateur en action. 

    Actions possibles:
    -go_chat -> messages , chat , discussions
    -go_lessons -> leçons , cours
    -go_top -> classement , leadearboard , top
    -go_profil -> profil , parametres 
    -go_boutique -> boutique , shop
    -go_dictionnaire -> dictionnaire
    -go_mylann -> mylann , milann , ia , assistant , traduction
    -unkown -> si tu ne comprends pas

    Regles:
    -Reponds uniquement en JSOn
    -Format exact : {{
    "action" : "..."
    }}

    Exemples:
    Phrase : "ouvre la boutique" -> {{"action" : "go_boutique"}}
    Phrase : "va sur mon profil" -> {{"action" : "go_profil"}} 

    Phrase : "{text}"
    """
    try:
        client = _load_openai_client()
        if client is None:
            return basic_rules(text)

        #Appel à l'ia
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":"tu es un assistant vocal qui repond uniquement en JSON"
                },
                {
                    "role" : "user",
                    "content" :prompt
                }
            ] ,
            temperature=0
        )
        #Recuperation du contenu de la reponse
        content = response.choices[0].message.content
        #Convertion JSON en dictionnaire python
        data = json.loads(content)
        return data
    except Exception as e:
        print("erreur IA" , e)
        return basic_rules(text)

def basic_rules(text : str):
    """Fonction simple , si l'ia marche pas"""
    text = text.lower()

    if "message" in text or "chat" in text or "discussions" in text:
        return {"action": "go_chat"}
    if "leçon" in text or "lecons" in text or "cours" in text:
        return {"action": "go_lessons"}
    if "classement" in text or "leaderboard" in text or "top" in text:
        return {"action": "go_top"}
    if "profil" in text or "parametre" in text or "paramètre" in text:
        return {"action": "go_profil"}
    if "boutique" in text or "shop" in text:
        return {"action": "go_boutique"}
    if "dictionnaire" in text:
        return {"action": "go_dictionnaire"}
    if "mylann" in text or "milann" in text or "ia" in text or "assistant" in text or "traduction" in text:
        return {"action": "go_mylann"}
    return {"action": "unkown"}