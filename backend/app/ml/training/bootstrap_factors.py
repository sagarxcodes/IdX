from __future__ import annotations

import json
from pathlib import Path


OUTPUT = Path(
    "data/training/bootstrap/factor_discovery.jsonl"
)


def example(
    case_id,
    objective,
    facts,
    factor_id,
    factor_name,
    category,
    relevant,
    importance,
    uncertainty,
):
    return {
        "case_id": case_id,
        "case_state": {
            "objective": objective,
            "facts": facts,
        },
        "factor": {
            "factor_id": factor_id,
            "name": factor_name,
            "category": category,
        },
        "labels": {
            "relevant": relevant,
            "importance": importance,
            "uncertainty": uncertainty,
        },
        "metadata": {
            "annotation_type": "expert_bootstrap",
            "source": "initial_expert_bootstrap",
        },
    }


def main():
    examples = [

        # -----------------------------------------------------
        # HOTEL
        # -----------------------------------------------------

        example(
            "hotel_001",
            "Determine whether the proposed hotel is commercially viable.",
            {
                "business_type": "hotel",
                "location": "near Chennai airport",
                "room_price": "₹8,000/night",
                "target_customer": "business travelers",
            },
            "hotel_demand",
            "local demand",
            "market",
            True,
            0.96,
            0.80,
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
            "hotel_logo_color",
            "logo color",
            "branding",
            False,
            0.01,
            0.10,
        ),

        # -----------------------------------------------------
        # ENGINEERING
        # -----------------------------------------------------

        example(
            "engineering_001",
            "Determine whether the proposed powered exoskeleton is technically feasible.",
            {
                "system": "powered exoskeleton",
                "goal": "assist human movement",
            },
            "exo_power_density",
            "power density",
            "energy",
            True,
            0.98,
            0.90,
        ),

        example(
            "engineering_001",
            "Determine whether the proposed powered exoskeleton is technically feasible.",
            {
                "system": "powered exoskeleton",
                "goal": "assist human movement",
            },
            "exo_color",
            "exoskeleton color",
            "design",
            False,
            0.00,
            0.05,
        ),

        # -----------------------------------------------------
        # SAAS
        # -----------------------------------------------------

        example(
            "saas_001",
            "Determine whether the proposed SaaS product has a viable market.",
            {
                "product": "workflow automation SaaS",
                "target_customer": "small businesses",
            },
            "saas_customer_pain",
            "customer pain",
            "customer",
            True,
            0.97,
            0.85,
        ),

        example(
            "saas_001",
            "Determine whether the proposed SaaS product has a viable market.",
            {
                "product": "workflow automation SaaS",
                "target_customer": "small businesses",
            },
            "saas_founder_language",
            "founder's preferred programming language",
            "implementation",
            False,
            0.02,
            0.10,
        ),
    ]

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as f:
        for item in examples:
            f.write(
                json.dumps(
                    item,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print(
        f"Wrote {len(examples)} examples to {OUTPUT}"
    )


if __name__ == "__main__":
    main()
