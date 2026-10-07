import os

import numpy as np
import evaluate
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    TrainingArguments,
    Trainer,
)


MODEL_NAME = "microsoft/deberta-v3-base"
OUTPUT_DIR = "data/training/models/idx-ner-v0"

MAX_LENGTH = 128


print("=" * 70)
print("IdX NER TRAINING")
print("=" * 70)

print("\nLoading CoNLL-2003...")

dataset = load_dataset("lhoestq/conll2003")

print(dataset)


label_names = [
    "O",
    "B-PER",
    "I-PER",
    "B-ORG",
    "I-ORG",
    "B-LOC",
    "I-LOC",
    "B-MISC",
    "I-MISC",
]

print("\nNER labels:")
for index, label in enumerate(label_names):
    print(f"{index:2d}  {label}")


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=True,
)


def tokenize_and_align_labels(example):

    tokenized = tokenizer(
        example["tokens"],
        truncation=True,
        max_length=MAX_LENGTH,
        is_split_into_words=True,
    )

    word_ids = tokenized.word_ids()

    labels = []

    previous_word_id = None

    for word_id in word_ids:

        if word_id is None:
            labels.append(-100)

        elif word_id != previous_word_id:
            labels.append(
                example["ner_tags"][word_id]
            )

        else:
            # Only label the first subword.
            labels.append(-100)

        previous_word_id = word_id

    tokenized["labels"] = labels

    return tokenized


print("\nTokenizing dataset...")

tokenized_dataset = dataset.map(
    tokenize_and_align_labels,
    batched=False,
)

print("Tokenization complete.")


seqeval = evaluate.load("seqeval")


def compute_metrics(eval_prediction):

    predictions, labels = eval_prediction

    predictions = np.argmax(
        predictions,
        axis=2,
    )

    true_predictions = []
    true_labels = []

    for prediction, label in zip(
        predictions,
        labels,
    ):

        current_predictions = []
        current_labels = []

        for pred, lab in zip(
            prediction,
            label,
        ):

            if lab == -100:
                continue

            current_predictions.append(
                label_names[pred]
            )

            current_labels.append(
                label_names[lab]
            )

        true_predictions.append(
            current_predictions
        )

        true_labels.append(
            current_labels
        )

    results = seqeval.compute(
        predictions=true_predictions,
        references=true_labels,
    )

    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


print("\nLoading DeBERTa token-classification model...")

model = AutoModelForTokenClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(label_names),
    id2label={
        i: label
        for i, label in enumerate(label_names)
    },
    label2id={
        label: i
        for i, label in enumerate(label_names)
    },
)

# Memory-efficient baseline:
# Freeze the pretrained DeBERTa encoder and train only
# the token-classification head.
for parameter in model.deberta.parameters():
    parameter.requires_grad = False

print("\nEncoder frozen: True")
print("Trainable parameters:")
trainable = 0
total = 0

for parameter in model.parameters():
    total += parameter.numel()
    if parameter.requires_grad:
        trainable += parameter.numel()

print(f"  trainable: {trainable:,}")
print(f"  total:     {total:,}")
print(f"  ratio:     {100.0 * trainable / total:.4f}%")


data_collator = DataCollatorForTokenClassification(
    tokenizer=tokenizer,
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True,
)


training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    learning_rate=2e-5,

    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,

    num_train_epochs=1,

    gradient_accumulation_steps=4,

    weight_decay=0.01,

    eval_strategy="epoch",
    save_strategy="epoch",

    logging_steps=100,

    report_to="none",

    save_total_limit=2,

    load_best_model_at_end=True,

    metric_for_best_model="f1",

    greater_is_better=True,

    dataloader_pin_memory=False,
)


trainer = Trainer(
    model=model,
    args=training_args,

    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],

    processing_class=tokenizer,

    data_collator=data_collator,

    compute_metrics=compute_metrics,
)


print("\nStarting training...")
print("This is the first real IdX NER training run.")
print()


trainer.train()


print("\nEvaluating on validation set...")

metrics = trainer.evaluate()

print("\nVALIDATION RESULTS")
print("=" * 70)

for key, value in metrics.items():

    if isinstance(value, float):
        print(
            f"{key:25} {value:.4f}"
        )
    else:
        print(
            f"{key:25} {value}"
        )


print("\nSaving final model...")

trainer.save_model(
    OUTPUT_DIR
)

tokenizer.save_pretrained(
    OUTPUT_DIR
)


print("\n" + "=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)

print("Model:", OUTPUT_DIR)
print("Base:", MODEL_NAME)

print("\nNext stage:")
print("Evaluate on held-out test data.")
print("Then perform IdX domain adaptation.")
