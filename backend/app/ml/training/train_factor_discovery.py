from __future__ import annotations

import json
import random
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer

from app.ml.models.factor_discovery_model import (
    IdXFactorDiscoveryModel,
)


DATA_PATH = Path(
    "data/training/factor_corpus/factors.jsonl"
)

OUTPUT_DIR = Path(
    "data/training/models/factor-discovery-v0-bootstrap"
)

MODEL_NAME = "microsoft/deberta-v3-base"

MAX_LENGTH = 256
BATCH_SIZE = 2
EPOCHS = 5
LEARNING_RATE = 2e-4
SEED = 42


class FactorDataset(Dataset):

    def __init__(self, records, tokenizer):
        self.records = records
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):

        record = self.records[index]

        case = record["case_state"]
        factor = record["factor"]
        labels = record["labels"]

        text = (
            f"domain: {case.get('domain', '')}. "
            f"industry: {case.get('industry', '')}. "
            f"archetype: {case.get('archetype', '')}. "
            f"objective: {case.get('objective', '')}. "
            f"facts: {json.dumps(case.get('facts', {}), ensure_ascii=False)}. "
            f"candidate factor: {factor.get('name', '')}. "
            f"factor category: {factor.get('category', '')}."
        )

        encoded = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )

        return {
            "input_ids": encoded["input_ids"].squeeze(0),
            "attention_mask": encoded["attention_mask"].squeeze(0),
            "relevant": torch.tensor(
                float(labels["relevant"]),
                dtype=torch.float32,
            ),
            "importance": torch.tensor(
                float(labels["importance"]),
                dtype=torch.float32,
            ),
        }


def load_records():

    with DATA_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]


def split_records(records):

    random.Random(SEED).shuffle(records)

    n = len(records)

    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    return (
        records[:train_end],
        records[train_end:val_end],
        records[val_end:],
    )


def evaluate(model, loader, device):

    model.eval()

    relevance_loss_fn = nn.BCEWithLogitsLoss()
    importance_loss_fn = nn.MSELoss()

    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():

        for batch in loader:

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)

            relevant = batch["relevant"].to(device)
            importance = batch["importance"].to(device)

            output = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

            relevance_loss = relevance_loss_fn(
                output["relevance_logit"],
                relevant,
            )

            importance_loss = importance_loss_fn(
                output["importance"],
                importance,
            )

            loss = (
                relevance_loss
                + importance_loss
            )

            total_loss += loss.item()

            predictions = (
                torch.sigmoid(
                    output["relevance_logit"]
                ) >= 0.5
            )

            correct += (
                predictions == relevant.bool()
            ).sum().item()

            total += len(relevant)

    return (
        total_loss / max(len(loader), 1),
        correct / max(total, 1),
    )


def main():

    random.seed(SEED)
    torch.manual_seed(SEED)

    device = torch.device(
        "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )

    print("=== IdX Factor Discovery Training ===")
    print(f"Device: {device}")
    print(f"Model:  {MODEL_NAME}")

    records = load_records()

    train_records, val_records, test_records = (
        split_records(records)
    )

    print(f"Total examples: {len(records)}")
    print(f"Train examples: {len(train_records)}")
    print(f"Validation:     {len(val_records)}")
    print(f"Test:           {len(test_records)}")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        use_fast=True,
    )

    train_dataset = FactorDataset(
        train_records,
        tokenizer,
    )

    val_dataset = FactorDataset(
        val_records,
        tokenizer,
    )

    test_dataset = FactorDataset(
        test_records,
        tokenizer,
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    model = IdXFactorDiscoveryModel(
        MODEL_NAME
    )

    # Memory-safe bootstrap training.
    for parameter in model.encoder.parameters():
        parameter.requires_grad = False

    model.to(device)

    trainable = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    total = sum(
        p.numel()
        for p in model.parameters()
    )

    print(
        f"Trainable parameters: {trainable:,}"
    )

    print(
        f"Total parameters:      {total:,}"
    )

    optimizer = torch.optim.AdamW(
        filter(
            lambda p: p.requires_grad,
            model.parameters(),
        ),
        lr=LEARNING_RATE,
    )

    relevance_loss_fn = nn.BCEWithLogitsLoss()
    importance_loss_fn = nn.MSELoss()

    for epoch in range(EPOCHS):

        model.train()

        total_loss = 0.0

        for batch_index, batch in enumerate(
            train_loader,
            start=1,
        ):

            optimizer.zero_grad()

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)

            relevant = batch["relevant"].to(device)
            importance = batch["importance"].to(device)

            output = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

            relevance_loss = relevance_loss_fn(
                output["relevance_logit"],
                relevant,
            )

            importance_loss = importance_loss_fn(
                output["importance"],
                importance,
            )

            loss = (
                relevance_loss
                + importance_loss
            )

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            print(
                f"epoch={epoch + 1} "
                f"batch={batch_index}/{len(train_loader)} "
                f"loss={loss.item():.4f}"
            )

        train_loss = (
            total_loss / len(train_loader)
        )

        val_loss, val_accuracy = evaluate(
            model,
            val_loader,
            device,
        )

        print(
            f"Epoch {epoch + 1}"
        )

        print(
            f"  train_loss={train_loss:.4f}"
        )

        print(
            f"  val_loss={val_loss:.4f}"
        )

        print(
            f"  val_relevance_accuracy="
            f"{val_accuracy:.4f}"
        )

    test_loss, test_accuracy = evaluate(
        model,
        test_loader,
        device,
    )

    print()
    print("=== FINAL TEST ===")
    print(f"test_loss={test_loss:.4f}")
    print(
        f"test_relevance_accuracy="
        f"{test_accuracy:.4f}"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    torch.save(
        model.state_dict(),
        OUTPUT_DIR / "model.pt",
    )

    tokenizer.save_pretrained(
        OUTPUT_DIR
    )

    print()
    print(
        f"Saved model to {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()
