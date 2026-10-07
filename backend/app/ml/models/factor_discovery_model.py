from __future__ import annotations

import torch
from torch import nn
from transformers import AutoModel


class IdXFactorDiscoveryModel(nn.Module):
    """
    Learned factor relevance and importance model.

    Input:
        case representation + candidate factor

    Output:
        relevance probability
        importance score
    """

    def __init__(
        self,
        model_name: str = "microsoft/deberta-v3-base",
    ):
        super().__init__()

        self.encoder = AutoModel.from_pretrained(model_name)

        hidden_size = self.encoder.config.hidden_size

        self.relevance_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.GELU(),
            nn.Dropout(0.15),
            nn.Linear(hidden_size // 2, 1),
        )

        self.importance_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.GELU(),
            nn.Dropout(0.15),
            nn.Linear(hidden_size // 2, 1),
            nn.Sigmoid(),
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

        relevance_logit = self.relevance_head(
            representation
        ).squeeze(-1)

        importance = self.importance_head(
            representation
        ).squeeze(-1)

        return {
            "relevance_logit": relevance_logit,
            "importance": importance,
        }
