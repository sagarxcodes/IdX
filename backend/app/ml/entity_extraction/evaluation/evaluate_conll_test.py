import os

import numpy as np
import torch
from datasets import load_dataset
from seqeval.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
)

MODEL_DIR = "data/training/models/idx-ner-v0"
MODEL_NAME = MODEL_DIR
MAX_LENGTH = 128

LABEL_NAMES = [
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


def tokenize_and_align_labels(example, tokenizer):
    tokenized = tokenizer(
        example["tokens"],
        is_split_into_words=True,
        truncation=True,
        max_length=MAX_LENGTH,
    )

    word_ids = tokenized.word_ids()
    labels = []
    previous_word_id = None

    for word_id in word_ids:
        if word_id is None:
            labels.append(-100)
        elif word_id != previous_word_id:
            labels.append(example["ner_tags"][word_id])
        else:
            labels.append(-100)

        previous_word_id = word_id

    tokenized["labels"] = labels
    return tokenized


def main():
    print("=" * 70)
    print("IdX NER — HELD-OUT TEST EVALUATION")
    print("=" * 70)

    if not os.path.exists(
        os.path.join(MODEL_DIR, "model.safetensors")
    ):
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_DIR}"
        )

    print("\nLoading CoNLL-2003 test set...")
    dataset = load_dataset("lhoestq/conll2003")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_DIR,
        use_fast=True,
    )

    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_DIR
    )

    device = torch.device(
        "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )

    model.to(device)
    model.eval()

    print(f"Device: {device}")

    print("\nTokenizing test set...")

    test_dataset = dataset["test"].map(
        lambda example: tokenize_and_align_labels(
            example,
            tokenizer,
        )
    )

    predictions = []
    references = []

    print("\nRunning inference...")

    with torch.no_grad():
        for index, example in enumerate(test_dataset):
            input_ids = torch.tensor(
                [example["input_ids"]],
                dtype=torch.long,
                device=device,
            )

            attention_mask = torch.tensor(
                [example["attention_mask"]],
                dtype=torch.long,
                device=device,
            )

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

            predicted_ids = (
                torch.argmax(
                    outputs.logits,
                    dim=-1,
                )
                .squeeze(0)
                .cpu()
                .numpy()
            )

            labels = np.array(example["labels"])

            pred_sequence = []
            ref_sequence = []

            for pred_id, label_id in zip(
                predicted_ids,
                labels,
            ):
                if label_id == -100:
                    continue

                pred_sequence.append(
                    LABEL_NAMES[int(pred_id)]
                )
                ref_sequence.append(
                    LABEL_NAMES[int(label_id)]
                )

            predictions.append(pred_sequence)
            references.append(ref_sequence)

            if (index + 1) % 500 == 0:
                print(
                    f"  {index + 1}/{len(test_dataset)}"
                )

    precision = precision_score(
        references,
        predictions,
    )

    recall = recall_score(
        references,
        predictions,
    )

    f1 = f1_score(
        references,
        predictions,
    )

    print("\n")
    print("=" * 70)
    print("HELD-OUT TEST RESULTS")
    print("=" * 70)

    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1        : {f1:.4f}")

    print("\nENTITY-LEVEL REPORT")
    print("=" * 70)

    print(
        classification_report(
            references,
            predictions,
            digits=4,
            zero_division=0,
        )
    )

    print("=" * 70)
    print("Evaluation complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
