import torch
from torch import nn
from transformers import AutoModel


class IdXEntityExtractionModel(nn.Module):

    def __init__(
        self,
        model_name="microsoft/deberta-v3-base",
        num_labels=32,
    ):

        super().__init__()

        self.encoder = AutoModel.from_pretrained(
            model_name
        )

        hidden_size = (
            self.encoder.config.hidden_size
        )

        self.dropout = nn.Dropout(0.1)

        self.classifier = nn.Linear(
            hidden_size,
            num_labels,
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

        representation = self.dropout(
            outputs.last_hidden_state
        )

        logits = self.classifier(
            representation
        )

        return logits
