import os
import importlib

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()

_model = None
_tokenizer = None

HF_MODEL = "aymericnzo/ivox_fr-dioula"


def _fallback_translation_message(text: str) -> str:
    return f"Je peux traduire '{text}', mais le modèle Dioula n'est pas disponible pour le moment."

def load_model():
    """Charge le modèle FR→Dioula depuis Hugging Face si ce n'est pas déjà fait."""
    global _model, _tokenizer

    if _model is not None:
        return _model, _tokenizer

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN manquant: impossible de charger le modèle de traduction.")

    transformers_module = importlib.import_module("transformers")
    AutoTokenizer = transformers_module.AutoTokenizer
    AutoModelForSeq2SeqLM = transformers_module.AutoModelForSeq2SeqLM

    # Charger depuis Hugging Face avec token moderne
    _tokenizer = AutoTokenizer.from_pretrained(HF_MODEL, token=hf_token)
    _model = AutoModelForSeq2SeqLM.from_pretrained(HF_MODEL, token=hf_token)

    return _model, _tokenizer

def translate(text: str) -> str:
    """Traduit une phrase du français vers le dioula."""
    # Protection: ne chargez le modèle HF que si l'option est explicitement activée
    # (évite les plantages natifs dus à torch/transformers sur des environnements limités).
    if os.getenv("ENABLE_HF_MODEL", "0") != "1":
        return _fallback_translation_message(text)

    try:
        model, tokenizer = load_model()
    except Exception:
        return _fallback_translation_message(text)

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