from typing import Dict, List

import torch
from transformers import AutoTokenizer

from app.ml.models.question_ranker_model import IdXQuestionRanker


class MLQuestionRanker:

    def __init__(
        self,
        model_name="microsoft/deberta-v3-base",
        device=None,
    ):
        self.model_name = model_name

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=False,
        )

        self.device = device or torch.device(
            "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        self.model = IdXQuestionRanker(
            model_name=model_name
        ).to(self.device)

        self.model.eval()

    def rank(
        self,
        case_state: str,
        candidates: List[Dict[str, str]],
    ):
        if not candidates:
            return []

        texts = [
            f"CASE:\n{case_state}\n\nQUESTION:\n{candidate['text']}"
            for candidate in candidates
        ]

        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )

        encoded = {
            key: value.to(self.device)
            for key, value in encoded.items()
        }

        with torch.no_grad():
            scores = self.model(**encoded)

        ranked = []

        for candidate, score in zip(
            candidates,
            scores.detach().cpu().tolist(),
        ):
            ranked.append({
                **candidate,
                "score": float(score),
            })

        ranked.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return ranked
