import torch
from torch import nn
from transformers import AutoModel


class IdXQuestionRanker(nn.Module):
    """
    Cross-encoder question/action ranking model.

    Input:
        CASE STATE + CANDIDATE QUESTION

    Output:
        learned utility score
    """

    def __init__(
        self,
        model_name="microsoft/deberta-v3-base",
    ):
        super().__init__()

        self.encoder = AutoModel.from_pretrained(
            model_name
        )

        hidden_size = self.encoder.config.hidden_size

        self.scorer = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.GELU(),
            nn.Dropout(0.15),
            nn.Linear(hidden_size // 2, 1),
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

        score = self.scorer(
            representation
        ).squeeze(-1)

        return score
