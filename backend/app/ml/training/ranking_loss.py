import torch
from torch import nn


class PairwiseRankingLoss(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(
        self,
        preferred_score,
        rejected_score,
    ):
        difference = (
            preferred_score
            - rejected_score
        )

        return torch.nn.functional.softplus(
            -difference
        ).mean()
