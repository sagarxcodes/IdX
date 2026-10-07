from __future__ import annotations

from typing import Any, Dict, List

from app.ml.factor_discovery.candidate_store import (
    FactorCandidateStore,
)
from app.ml.factor_discovery.retriever import (
    FactorRetriever,
)
from app.ml.factor_discovery.predictor import (
    FactorPredictor,
)


class FactorDiscoveryService:

    def __init__(
        self,
        corpus_path: str,
        checkpoint_dir: str,
        retrieval_top_k: int = 20,
    ):
        self.store = FactorCandidateStore(
            corpus_path
        )

        self.retriever = FactorRetriever()

        self.predictor = FactorPredictor(
            checkpoint_dir
        )

        self.retrieval_top_k = retrieval_top_k

    def discover(
        self,
        case: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        candidates = self.retriever.retrieve(
            case,
            self.store.all(),
            top_k=self.retrieval_top_k,
        )

        return self.predictor.predict(
            case,
            candidates,
        )
