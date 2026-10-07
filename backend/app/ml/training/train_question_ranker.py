from __future__ import annotations

import json
from pathlib import Path

import torch
from torch import nn
from transformers import (
    AutoTokenizer,
    AutoModel,
)


MODEL_NAME = "microsoft/deberta-v3-base"

DATA_DIR = Path(
    "data/training/bootstrap/splits"
)

OUTPUT_DIR = Path(
    "data/training/models/question-ranker-v0"
)

MAX_LENGTH = 256
EPOCHS = 2
LEARNING_RATE = 2e-5


class PairwiseRanker(nn.Module):
    def __init__(self):
        super().__init__()

        self.encoder = AutoModel.from_pretrained(
            MODEL_NAME
        )

        hidden = self.encoder.config.hidden_size

        self.dropout = nn.Dropout(0.1)

        self.scorer = nn.Sequential(
            nn.Linear(hidden, hidden // 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden // 2, 1),
        )

    def forward(
        self,
        input_ids,
        attention_mask,
        **kwargs,
    ):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )

        representation = outputs.last_hidden_state[:, 0]

        representation = self.dropout(
            representation
        )

        return self.scorer(
            representation
        ).squeeze(-1)


def load_pairs(path):
    pairs = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pairs.append(json.loads(line))

    return pairs


def make_text(case_state, action):
    return (
        "CASE\n"
        f"Objective: {case_state.get('objective', '')}\n"
        f"Facts: {json.dumps(case_state.get('facts', {}), ensure_ascii=False)}\n"
        f"Unknowns: {json.dumps(case_state.get('unknowns', []), ensure_ascii=False)}\n\n"
        "ACTION\n"
        f"Type: {action.get('action_type', '')}\n"
        f"Description: {action.get('description', '')}"
    )


def encode_pair(tokenizer, pair, device):
    preferred_text = make_text(
        pair["case_state"],
        pair["preferred_action"],
    )

    rejected_text = make_text(
        pair["case_state"],
        pair["rejected_action"],
    )

    preferred = tokenizer(
        preferred_text,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    rejected = tokenizer(
        rejected_text,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    preferred = {
        k: v.to(device)
        for k, v in preferred.items()
    }

    rejected = {
        k: v.to(device)
        for k, v in rejected.items()
    }

    return preferred, rejected


def pairwise_loss(preferred_score, rejected_score):
    return torch.nn.functional.softplus(
        -(preferred_score - rejected_score)
    ).mean()


def evaluate(model, tokenizer, pairs, device):
    if not pairs:
        return None

    model.eval()

    correct = 0
    losses = []

    with torch.no_grad():
        for pair in pairs:
            preferred, rejected = encode_pair(
                tokenizer,
                pair,
                device,
            )

            preferred_score = model(**preferred)
            rejected_score = model(**rejected)

            loss = pairwise_loss(
                preferred_score,
                rejected_score,
            )

            losses.append(loss.item())

            if (
                preferred_score.item()
                > rejected_score.item()
            ):
                correct += 1

    return {
        "accuracy": correct / len(pairs),
        "loss": sum(losses) / len(losses),
    }


def main():
    device = torch.device(
        "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )

    print("=== IdX Question Ranker Training ===")
    print(f"Device: {device}")
    print(f"Model:  {MODEL_NAME}")

    train_pairs = load_pairs(
        DATA_DIR / "train.jsonl"
    )

    validation_pairs = load_pairs(
        DATA_DIR / "validation.jsonl"
    )

    test_pairs = load_pairs(
        DATA_DIR / "test.jsonl"
    )

    print(f"Train pairs:      {len(train_pairs)}")
    print(f"Validation pairs: {len(validation_pairs)}")
    print(f"Test pairs:       {len(test_pairs)}")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        use_fast=False,
    )

    model = PairwiseRanker().to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=0.01,
    )

    for epoch in range(EPOCHS):
        model.train()

        total_loss = 0.0

        for index, pair in enumerate(
            train_pairs,
            start=1,
        ):
            preferred, rejected = encode_pair(
                tokenizer,
                pair,
                device,
            )

            preferred_score = model(**preferred)
            rejected_score = model(**rejected)

            loss = pairwise_loss(
                preferred_score,
                rejected_score,
            )

            optimizer.zero_grad()
            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                1.0,
            )

            optimizer.step()

            total_loss += loss.item()

            print(
                f"epoch={epoch + 1} "
                f"pair={index}/{len(train_pairs)} "
                f"loss={loss.item():.4f}"
            )

        train_loss = (
            total_loss / len(train_pairs)
        )

        validation = evaluate(
            model,
            tokenizer,
            validation_pairs,
            device,
        )

        print(
            f"\nEpoch {epoch + 1}"
            f"\n  train_loss={train_loss:.4f}"
        )

        if validation:
            print(
                f"  val_loss={validation['loss']:.4f}"
                f"\n  val_pair_accuracy="
                f"{validation['accuracy']:.4f}"
            )

    test = evaluate(
        model,
        tokenizer,
        test_pairs,
        device,
    )

    print("\n=== FINAL TEST ===")
    print(
        f"test_loss={test['loss']:.4f}"
    )
    print(
        f"test_pair_accuracy="
        f"{test['accuracy']:.4f}"
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

    print(
        f"\nSaved model to {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()
