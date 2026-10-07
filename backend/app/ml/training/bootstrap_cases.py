from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


OUTPUT = Path("data/training/bootstrap/question_ranking.jsonl")


def example(
    case_id: str,
    objective: str,
    facts: Dict[str, Any],
    unknowns: List[str],
    action_id: str,
    action_type: str,
    description: str,
    preferred: bool,
    information_gain: float,
    decision_impact: float,
    evidence_value: float,
    uncertainty_reduction: float,
    user_effort: float,
    annotation_type: str = "expert_bootstrap",
) -> Dict[str, Any]:

    return {
        "case_id": case_id,
        "case_state": {
            "objective": objective,
            "facts": facts,
            "unknowns": unknowns,
        },
        "candidate_action": {
            "action_id": action_id,
            "action_type": action_type,
            "description": description,
        },
        "labels": {
            "preferred": preferred,
            "information_gain": information_gain,
            "decision_impact": decision_impact,
            "evidence_value": evidence_value,
            "uncertainty_reduction": uncertainty_reduction,
            "user_effort": user_effort,
        },
        "metadata": {
            "annotation_type": annotation_type,
            "source": "initial_expert_bootstrap",
        },
    }


def build() -> None:
    examples = [

        # ---------------------------------------------------------
        # HOTEL
        # ---------------------------------------------------------

        example(
            "hotel_001",
            "Determine whether the proposed hotel is commercially viable.",
            {
                "business_type": "hotel",
                "location": "near Chennai airport",
                "room_price": "₹8,000/night",
                "target_customer": "business travelers",
            },
            [
                "competitor pricing",
                "local demand",
                "expected occupancy",
                "operating costs",
            ],
            "hotel_001_a",
            "research",
            "Research comparable hotels near the airport and their room prices.",
            True,
            0.92, 0.94, 0.93, 0.88, 0.20,
        ),

        example(
            "hotel_001",
            "Determine whether the proposed hotel is commercially viable.",
            {
                "business_type": "hotel",
                "location": "near Chennai airport",
                "room_price": "₹8,000/night",
                "target_customer": "business travelers",
            },
            [
                "competitor pricing",
                "local demand",
                "expected occupancy",
                "operating costs",
            ],
            "hotel_001_b",
            "question",
            "Ask which hotel brand the owner personally likes.",
            False,
            0.05, 0.02, 0.01, 0.03, 0.05,
        ),

        # ---------------------------------------------------------
        # RESTAURANT
        # ---------------------------------------------------------

        example(
            "restaurant_001",
            "Determine whether opening the restaurant is financially viable.",
            {
                "business_type": "restaurant",
                "location": "Bengaluru",
                "concept": "premium vegetarian restaurant",
            },
            [
                "target customer",
                "competitor pricing",
                "rent",
                "expected daily customers",
                "average order value",
            ],
            "restaurant_001_a",
            "research",
            "Research nearby competitors, their pricing, ratings and customer positioning.",
            True,
            0.91, 0.90, 0.92, 0.87, 0.25,
        ),

        example(
            "restaurant_001",
            "Determine whether opening the restaurant is financially viable.",
            {
                "business_type": "restaurant",
                "location": "Bengaluru",
                "concept": "premium vegetarian restaurant",
            },
            [
                "target customer",
                "competitor pricing",
                "rent",
                "expected daily customers",
                "average order value",
            ],
            "restaurant_001_b",
            "question",
            "Ask what color the restaurant logo should use.",
            False,
            0.02, 0.01, 0.00, 0.01, 0.05,
        ),

        # ---------------------------------------------------------
        # SAAS
        # ---------------------------------------------------------

        example(
            "saas_001",
            "Determine whether the proposed SaaS product has a viable market.",
            {
                "product": "workflow automation SaaS",
                "target_customer": "small businesses",
                "pricing": "subscription",
            },
            [
                "customer pain",
                "existing alternatives",
                "willingness to pay",
                "market size",
                "retention potential",
            ],
            "saas_001_a",
            "research",
            "Investigate existing competitors and the problems customers complain about in current solutions.",
            True,
            0.93, 0.94, 0.91, 0.90, 0.30,
        ),

        example(
            "saas_001",
            "Determine whether the proposed SaaS product has a viable market.",
            {
                "product": "workflow automation SaaS",
                "target_customer": "small businesses",
                "pricing": "subscription",
            },
            [
                "customer pain",
                "existing alternatives",
                "willingness to pay",
                "market size",
                "retention potential",
            ],
            "saas_001_b",
            "question",
            "Ask which programming language the founder prefers.",
            False,
            0.04, 0.03, 0.01, 0.02, 0.05,
        ),

        # ---------------------------------------------------------
        # AGRICULTURE
        # ---------------------------------------------------------

        example(
            "agri_001",
            "Determine which crop strategy is most suitable for the farm.",
            {
                "farm_size": "2.5 acres",
                "location": "Tamil Nadu",
                "goal": "maximize profitable production",
            },
            [
                "soil condition",
                "water availability",
                "season",
                "local crop prices",
                "market demand",
            ],
            "agri_001_a",
            "research",
            "Determine current water availability and reliable soil measurements before recommending crops.",
            True,
            0.94, 0.95, 0.89, 0.94, 0.30,
        ),

        example(
            "agri_001",
            "Determine which crop strategy is most suitable for the farm.",
            {
                "farm_size": "2.5 acres",
                "location": "Tamil Nadu",
                "goal": "maximize profitable production",
            },
            [
                "soil condition",
                "water availability",
                "season",
                "local crop prices",
                "market demand",
            ],
            "agri_001_b",
            "question",
            "Ask what color the farmer wants for the dashboard.",
            False,
            0.01, 0.00, 0.00, 0.01, 0.05,
        ),

        # ---------------------------------------------------------
        # ENGINEERING
        # ---------------------------------------------------------

        example(
            "engineering_001",
            "Determine whether the proposed powered exoskeleton is technically feasible.",
            {
                "system": "powered exoskeleton",
                "goal": "assist human movement",
            },
            [
                "power source",
                "actuator capability",
                "system weight",
                "thermal constraints",
                "human safety",
            ],
            "engineering_001_a",
            "analysis",
            "Quantify the required power, actuator force, total system mass and operating duration.",
            True,
            0.96, 0.97, 0.85, 0.95, 0.45,
        ),

        example(
            "engineering_001",
            "Determine whether the proposed powered exoskeleton is technically feasible.",
            {
                "system": "powered exoskeleton",
                "goal": "assist human movement",
            },
            [
                "power source",
                "actuator capability",
                "system weight",
                "thermal constraints",
                "human safety",
            ],
            "engineering_001_b",
            "question",
            "Ask what color the exoskeleton should be.",
            False,
            0.00, 0.00, 0.00, 0.00, 0.02,
        ),
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as f:
        for item in examples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Wrote {len(examples)} examples to {OUTPUT}")


if __name__ == "__main__":
    build()
