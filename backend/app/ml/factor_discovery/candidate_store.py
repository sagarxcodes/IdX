from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class FactorCandidateStore:
    """
    Data-driven factor candidate store.

    Candidates are loaded from the factor corpus.
    No domain-specific question/factor rules live here.
    """

    def __init__(self, corpus_path: str):
        self.corpus_path = Path(corpus_path)
        self._factors: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not self.corpus_path.exists():
            raise FileNotFoundError(
                f"Factor corpus not found: {self.corpus_path}"
            )

        with self.corpus_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            for line in f:
                if not line.strip():
                    continue

                record = json.loads(line)
                factor = record["factor"]

                factor_id = factor["factor_id"]

                if factor_id not in self._factors:
                    self._factors[factor_id] = {
                        "factor_id": factor_id,
                        "name": factor["name"],
                        "category": factor.get(
                            "category",
                            "unknown",
                        ),
                    }

    def all(self) -> List[Dict[str, Any]]:
        return list(self._factors.values())

    def __len__(self) -> int:
        return len(self._factors)
