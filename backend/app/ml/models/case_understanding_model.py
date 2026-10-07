import torch
from torch import nn
from transformers import AutoModel


class IdXCaseUnderstandingModel(nn.Module):
    """
    Multi-task transformer for IdX case understanding.

    Shared DeBERTa representation
             |
             +-- domain classification
             +-- archetype classification
             +-- objective representation
             +-- constraint representation
    """

    def __init__(
        self,
        model_name="microsoft/deberta-v3-base",
        num_domains=12,
        num_archetypes=16,
    ):
        super().__init__()

        self.encoder = AutoModel.from_pretrained(
            model_name
        )

        hidden_size = self.encoder.config.hidden_size

        self.dropout = nn.Dropout(0.15)

        self.domain_head = nn.Linear(
            hidden_size,
            num_domains,
        )

        self.archetype_head = nn.Linear(
            hidden_size,
            num_archetypes,
        )

        self.objective_head = nn.Linear(
            hidden_size,
            hidden_size,
        )

        self.constraint_head = nn.Linear(
            hidden_size,
            hidden_size,
        )

    def forward(
        self,
        input_ids,
        attention_mask,
    ):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )

        representation = outputs.last_hidden_state[:, 0]

        representation = self.dropout(
            representation
        )

        return {
            "representation": representation,
            "domain_logits": self.domain_head(
                representation
            ),
            "archetype_logits": self.archetype_head(
                representation
            ),
            "objective_embedding": self.objective_head(
                representation
            ),
            "constraint_embedding": self.constraint_head(
                representation
            ),
        }
