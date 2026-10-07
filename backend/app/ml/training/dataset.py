import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List

from app.ml.training_schema import MLTrainingExample


class TrainingDataset:

    def __init__(self):
        self.examples: List[MLTrainingExample] = []

    def add(self, example: MLTrainingExample):
        self.examples.append(example)

    def extend(self, examples: Iterable[MLTrainingExample]):
        self.examples.extend(examples)

    def __len__(self):
        return len(self.examples)

    def save_jsonl(self, path: str):

        output = Path(path)
        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output.open(
            "w",
            encoding="utf-8",
        ) as f:

            for example in self.examples:

                f.write(
                    json.dumps(
                        asdict(example),
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    @classmethod
    def load_jsonl(cls, path: str):

        dataset = cls()

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                data = json.loads(line)

                dataset.add(
                    MLTrainingExample(
                        **data
                    )
                )

        return dataset
