from typing import Dict, List

import torch
from transformers import AutoTokenizer

from app.ml.entity_extraction.labels import (
    ID_TO_LABEL,
)
from app.ml.entity_extraction.model import (
    IdXEntityExtractionModel,
)


class EntityExtractor:

    def __init__(
        self,
        model_name="microsoft/deberta-v3-base",
        device=None,
    ):

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                model_name,
                use_fast=False,
            )
        )

        self.device = device or torch.device(
            "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        self.model = (
            IdXEntityExtractionModel(
                model_name=model_name,
                num_labels=len(ID_TO_LABEL),
            )
            .to(self.device)
        )

        self.model.eval()

    def extract(
        self,
        text: str,
    ) -> List[Dict]:

        encoded = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )

        encoded = {
            key: value.to(self.device)
            for key, value in encoded.items()
        }

        with torch.no_grad():

            logits = self.model(
                **encoded
            )

        probabilities = torch.softmax(
            logits,
            dim=-1,
        )

        predictions = (
            probabilities.argmax(
                dim=-1
            )[0]
            .detach()
            .cpu()
            .tolist()
        )

        tokens = self.tokenizer.convert_ids_to_tokens(
            encoded["input_ids"][0]
            .detach()
            .cpu()
            .tolist()
        )

        entities = []

        for token, label_id in zip(
            tokens,
            predictions,
        ):

            label = ID_TO_LABEL[
                label_id
            ]

            if label != "O":

                entities.append(
                    {
                        "token": token,
                        "label": label,
                    }
                )

        return entities
