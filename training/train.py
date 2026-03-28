from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments

import os

# 1. Connexion Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")

# 2. Charger dataset (FR → DIOULA)
dataset = load_dataset("uvci/Koumankan_mt_dyu_fr", use_auth_token=HF_TOKEN)

# 3. Charger modèle pré-entraîné Seq2Seq
tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-fr-en")

# 4. Preprocess (tokenizer tous les exemples)
def preprocess(example):
    input_text = "Traduire en dioula : " + example["fr"]
    target_text = example["dyu"]

    model_inputs = tokenizer(input_text, max_length=128, truncation=True, padding="max_length")
    labels = tokenizer(target_text, max_length=128, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

dataset = dataset.map(preprocess)

# 5. Entraînement
training_args = TrainingArguments(
    output_dir="../model",
    per_device_train_batch_size=4,
    num_train_epochs=3
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"]
)

trainer.train()

# 6. Sauvegarde modèle
model.save_pretrained("../model")
tokenizer.save_pretrained("../model")