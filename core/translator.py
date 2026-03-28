from pathlib import Path

_translator = None

def _get_translator():
    """Charge le modèle FR→Dioula si ce n'est pas déjà fait."""
    global _translator
    if _translator is not None:
        return _translator

    # Chemin vers le dossier model/
    model_dir = Path(__file__).resolve().parent.parent / "model"

    if not model_dir.exists():
        return None

    try:
        from transformers import pipeline
    except Exception:
        return None

    # Crée le pipeline de traduction
    _translator = pipeline(
        task="translation",
        model=str(model_dir),
        tokenizer=str(model_dir),
    )
    return _translator

def translate(text: str) -> str:
    """
    Traduit une phrase du français vers le dioula.
    
    Args:
        text (str): texte en français

    Returns:
        str: texte traduit en dioula
    """
    translator = _get_translator()
    # Si le modèle est introuvable, retourne le texte original
    if translator is None:
        return text

    # Ajout d'une consigne pour le modèle
    prompt = f"Traduire en dioula : {text}"
    result = translator(prompt)

    # Le pipeline renvoie une liste, on prend le premier élément
    return result[0]["translation_text"]