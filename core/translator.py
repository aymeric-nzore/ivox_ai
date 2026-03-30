
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
from dotenv import load_dotenv

load_dotenv()

_model = None
_tokenizer = None

HF_MODEL = "aymericnzo/ivox_fr-dioula"
HF_TOKEN = os.getenv("HF_TOKEN")  # doit être défini dans l'environnement

if not HF_TOKEN:
    raise EnvironmentError("La variable d'environnement HF_TOKEN n'est pas définie. Ajoutez-la avant de lancer le script.")

def load_model():
    """Charge le modèle FR→Dioula depuis Hugging Face si ce n'est pas déjà fait."""
    global _model, _tokenizer

    if _model is not None:
        return _model, _tokenizer

    # Charger depuis Hugging Face avec token moderne
    _tokenizer = AutoTokenizer.from_pretrained(HF_MODEL, token=HF_TOKEN)
    _model = AutoModelForSeq2SeqLM.from_pretrained(HF_MODEL, token=HF_TOKEN)

    return _model, _tokenizer

def translate(text: str) -> str:
    """Traduit une phrase du français vers le dioula."""
    model, tokenizer = load_model()

    # Tokenizer input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    # Génération
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("dyu_Latn")
    generated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_length=128
    )

    # Décodage
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return result[0]