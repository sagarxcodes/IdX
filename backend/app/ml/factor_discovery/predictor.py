from __future__ import annotations

from typing import Any, Dict, List

import torch
from transformers import AutoTokenizer

from app.ml.models.factor_discovery_model import (
    IdXFactorDiscoveryModel,
)


class FactorPredictor:

    def __init__(
        self,
        checkpoint_dir: str,
        model_name: str = "microsoft/deberta-v3-base",
    ):
        self.device = torch.device(
            "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            checkpoint_dir,
            use_fast=True,
        )

        self.model = IdXFactorDiscoveryModel(
            model_name
        )

        state = torch.load(
            f"{checkpoint_dir}/model.pt",
            map_location="cpu",
        )

        self.model.load_state_dict(state)
        self.model.to(self.device)
        self.model.eval()

    def _text(
        self,
        case: Dict[str, Any],
        factor: Dict[str, Any],
    ) -> str:

        return (
            f"domain: {case.get('domain', '')}. "
            f"industry: {case.get('industry', '')}. "
            f"archetype: {case.get('archetype', '')}. "
            f"objective: {case.get('objective', '')}. "
            f"facts: {case.get('facts', {})}. "
            f"candidate factor: {factor.get('name', '')}. "
            f"factor category: {factor.get('category', '')}."
        )

    def predict(
        self,
        case: Dict[str, Any],
        factors: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        if not factors:
            return []

        texts = [
            self._text(case, factor)
            for factor in factors
        ]

        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt",
        )

        encoded = {
            key: value.to(self.device)
            for key, value in encoded.items()
        }

        with torch.no_grad():
            output = self.model(
                input_ids=encoded["input_ids"],
                attention_mask=encoded["attention_mask"],
            )

        relevance = torch.sigmoid(
            output["relevance_logit"]
        ).tolist()

        importance = (
            output["importance"]
            .tolist()
        )

        results = []

        for factor, rel, imp in zip(
            factors,
            relevance,
            importance,
        ):
            result = dict(factor)
            result["relevance"] = float(rel)
            result["importance"] = float(imp)
            results.append(result)

        results.sort(
            key=lambda x: (
                x["relevance"],
                x["importance"],
            ),
            reverse=True,
        )

        return results
