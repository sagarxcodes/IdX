from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelSpec:
    name: str
    version: str
    task: str
    architecture: str
    status: str = "untrained"


MODEL_REGISTRY: Dict[str, ModelSpec] = {

    "case_understanding": ModelSpec(
        name="case_understanding",
        version="0.1.0",
        task="multi_task_case_understanding",
        architecture="deberta_v3",
    ),

    "factor_discovery": ModelSpec(
        name="factor_discovery",
        version="0.1.0",
        task="factor_discovery",
        architecture="transformer",
    ),

    "question_ranking": ModelSpec(
        name="question_ranking",
        version="0.1.0",
        task="next_best_action_ranking",
        architecture="deberta_v3_cross_encoder",
    ),

    "evidence_ranking": ModelSpec(
        name="evidence_ranking",
        version="0.1.0",
        task="evidence_relevance",
        architecture="transformer",
    ),

    "similarity": ModelSpec(
        name="similarity",
        version="0.1.0",
        task="case_similarity",
        architecture="embedding_model",
    ),

    "contradiction": ModelSpec(
        name="contradiction",
        version="0.1.0",
        task="contradiction_detection",
        architecture="transformer",
    ),

    "feasibility": ModelSpec(
        name="feasibility",
        version="0.1.0",
        task="feasibility_prediction",
        architecture="multi_modal",
    ),

    "risk": ModelSpec(
        name="risk",
        version="0.1.0",
        task="risk_prediction",
        architecture="multi_task",
    ),

    "strategy": ModelSpec(
        name="strategy",
        version="0.1.0",
        task="strategy_generation_and_ranking",
        architecture="hybrid",
    ),

    "outcome": ModelSpec(
        name="outcome",
        version="0.1.0",
        task="outcome_prediction",
        architecture="temporal",
    ),
}
