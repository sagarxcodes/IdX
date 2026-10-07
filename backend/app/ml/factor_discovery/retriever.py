from __future__ import annotations

from typing import Any, Dict, List

import torch
from transformers import AutoModel, AutoTokenizer


class FactorRetriever:
    """
    Semantic factor candidate retrieval.

    This retrieves factors whose representations are
    semantically related to the case.

    It is intentionally independent of domain-specific rules.
    """

    def __init__(
        self,
        model_name: str = "microsoft/deberta-v3-base",
        device: str | None = None,
    ):
        self.device = torch.device(
            device
            if device
            else (
                "mps"
                if torch.backends.mps.is_available()
                else "cpu"
            )
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=True,
        )

        self.encoder = AutoModel.from_pretrained(
            model_name
        )

        self.encoder.to(self.device)
        self.encoder.eval()

    def _encode(self, texts: List[str]) -> torch.Tensor:

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
            output = self.encoder(**encoded)

        representation = output.last_hidden_state[:, 0]

        representation = torch.nn.functional.normalize(
            representation,
            p=2,
            dim=1,
        )

        return representation

    def _case_text(
        self,
        case: Dict[str, Any],
    ) -> str:

        return (
            f"domain: {case.get('domain', '')}. "
            f"industry: {case.get('industry', '')}. "
            f"archetype: {case.get('archetype', '')}. "
            f"objective: {case.get('objective', '')}. "
            f"facts: {case.get('facts', {})}."
        )

    def _factor_text(
        self,
        factor: Dict[str, Any],
    ) -> str:

        return (
            f"factor: {factor.get('name', '')}. "
            f"category: {factor.get('category', '')}."
        )

    def retrieve(
        self,
        case: Dict[str, Any],
        factors: List[Dict[str, Any]],
        top_k: int = 20,
    ) -> List[Dict[str, Any]]:

        if not factors:
            return []

        case_embedding = self._encode(
            [self._case_text(case)]
        )

        factor_embeddings = self._encode(
            [
                self._factor_text(factor)
                for factor in factors
            ]
        )

        similarities = torch.matmul(
            case_embedding,
            factor_embeddings.T,
        )[0]

        k = min(top_k, len(factors))

        values, indices = torch.topk(
            similarities,
            k=k,
        )

        results = []

        for score, index in zip(
            values.tolist(),
            indices.tolist(),
        ):
            result = dict(factors[index])
            result["retrieval_score"] = float(score)
            results.append(result)

        return results
