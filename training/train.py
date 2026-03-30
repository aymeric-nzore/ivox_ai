
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    HF_TOKEN = os.getenv("HF_TOKEN")
    # 🔥 Modèle Helsinki-NLP (plus léger)
    # Si fr-dyu n'existe pas, utiliser fr-en ou fr-mul comme base
    model_name = "Helsinki-NLP/opus-mt-fr-en"

    # 1. Charger dataset
    dataset = load_dataset("uvci/Koumankan_mt_dyu_fr", token=HF_TOKEN)

    # 2. Charger tokenizer + modèle (Helsinki-NLP n'a pas besoin de token)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # 3. Preprocess adapté Helsinki-NLP (définie ici pour accès à tokenizer)
    def preprocess(examples):
        inputs = [ex["fr"] for ex in examples["translation"]]
        targets = [ex["dyu"] for ex in examples["translation"]]

        model_inputs = tokenizer(
            inputs,
            max_length=64,
            truncation=True,
            padding="max_length"
        )

        labels = tokenizer(
            targets,
            max_length=64,
            truncation=True,
            padding="max_length"
        )

        labels["input_ids"] = [
            [(l if l != tokenizer.pad_token_id else -100) for l in label]
            for label in labels["input_ids"]
        ]

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    # 4. Appliquer preprocess
    dataset = dataset.map(preprocess, batched=True)

    # 5. Training config (optimisé CPU)
    training_args = TrainingArguments(
        output_dir="../model",
        per_device_train_batch_size=8,  # batch plus grand car modèle léger
        num_train_epochs=3,             # plus d'epochs car rapide
        logging_steps=20,
        save_steps=1000,
        save_total_limit=1,
        fp16=False,                     # pas de float16 sur CPU
        dataloader_num_workers=0        # important pour Windows !
    )

    # 6. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"]
    )

    print("Début de l'entraînement...")
    trainer.train()

    # 7. Sauvegarde
    model.save_pretrained("../model")
    tokenizer.save_pretrained("../model")