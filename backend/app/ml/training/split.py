import random
from typing import List, Tuple

from app.ml.training_schema import MLTrainingExample


def split_dataset(
    examples: List[MLTrainingExample],
    train_ratio: float = 0.8,
    validation_ratio: float = 0.1,
    seed: int = 42,
) -> Tuple[
    List[MLTrainingExample],
    List[MLTrainingExample],
    List[MLTrainingExample],
]:

    if train_ratio + validation_ratio >= 1.0:
        raise ValueError(
            "train_ratio + validation_ratio "
            "must be < 1.0"
        )

    examples = list(examples)

    rng = random.Random(seed)
    rng.shuffle(examples)

    total = len(examples)

    train_end = int(
        total * train_ratio
    )

    validation_end = train_end + int(
        total * validation_ratio
    )

    train = examples[:train_end]

    validation = examples[
        train_end:validation_end
    ]

    test = examples[
        validation_end:
    ]

    return train, validation, test
