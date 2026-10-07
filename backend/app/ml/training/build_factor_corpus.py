from __future__ import annotations

import json
from pathlib import Path


OUTPUT = Path("data/training/factor_corpus/factors.jsonl")


CASES = [
    {
        "case_id": "hospitality_001",
        "domain": "business",
        "industry": "hospitality",
        "archetype": "new_hotel",
        "objective": "Determine whether a premium airport hotel is commercially viable.",
        "facts": {
            "location": "near Chennai airport",
            "room_price": "₹8,000/night",
            "target_customer": "business travelers",
        },
        "factors": [
            ("local_demand", "market", True, 0.96, 0.80),
            ("competitor_pricing", "competition", True, 0.94, 0.75),
            ("business_traveler_spending", "customer", True, 0.91, 0.82),
            ("expected_occupancy", "economics", True, 0.97, 0.88),
            ("seasonality", "market", True, 0.82, 0.72),
            ("logo_color", "branding", False, 0.01, 0.10),
        ],
    },
    {
        "case_id": "restaurant_001",
        "domain": "business",
        "industry": "restaurant",
        "archetype": "new_restaurant",
        "objective": "Determine whether a premium restaurant can achieve sustainable profitability.",
        "facts": {
            "location": "urban commercial area",
            "positioning": "premium dining",
        },
        "factors": [
            ("local_customer_demand", "market", True, 0.95, 0.80),
            ("average_customer_spend", "customer", True, 0.91, 0.76),
            ("competitor_density", "competition", True, 0.87, 0.70),
            ("food_cost_ratio", "economics", True, 0.96, 0.85),
            ("table_turnover", "operations", True, 0.89, 0.78),
            ("menu_font", "branding", False, 0.01, 0.05),
        ],
    },
    {
        "case_id": "saas_001",
        "domain": "business",
        "industry": "software",
        "archetype": "new_saas",
        "objective": "Determine whether a proposed B2B SaaS product has a viable market.",
        "facts": {
            "customer": "small businesses",
            "model": "subscription",
        },
        "factors": [
            ("customer_pain", "customer", True, 0.98, 0.86),
            ("willingness_to_pay", "customer", True, 0.96, 0.88),
            ("market_size", "market", True, 0.89, 0.75),
            ("competitor_strength", "competition", True, 0.90, 0.79),
            ("customer_acquisition_cost", "economics", True, 0.94, 0.83),
            ("founder_preferred_language", "technology", False, 0.02, 0.10),
        ],
    },
    {
        "case_id": "market_001",
        "domain": "finance",
        "industry": "financial_markets",
        "archetype": "trading_strategy",
        "objective": "Determine whether a market signal has exploitable predictive value.",
        "facts": {
            "asset": "liquid equity",
            "horizon": "short term",
        },
        "factors": [
            ("signal_predictive_power", "market", True, 0.99, 0.90),
            ("transaction_costs", "execution", True, 0.95, 0.82),
            ("liquidity", "market", True, 0.94, 0.70),
            ("signal_decay", "strategy", True, 0.92, 0.86),
            ("regime_stability", "risk", True, 0.90, 0.91),
            ("dashboard_font", "presentation", False, 0.00, 0.02),
        ],
    },
    {
        "case_id": "agriculture_001",
        "domain": "agriculture",
        "industry": "farming",
        "archetype": "crop_production",
        "objective": "Determine the most economically suitable crop strategy for a farm.",
        "facts": {
            "farm_size": "2.5 acres",
            "region": "South India",
        },
        "factors": [
            ("soil_conditions", "production", True, 0.96, 0.78),
            ("water_availability", "resources", True, 0.98, 0.82),
            ("crop_market_price", "market", True, 0.94, 0.76),
            ("expected_yield", "production", True, 0.95, 0.88),
            ("weather_risk", "risk", True, 0.93, 0.91),
            ("farmers_favorite_color", "irrelevant", False, 0.00, 0.02),
        ],
    },
    {
        "case_id": "engineering_001",
        "domain": "engineering",
        "industry": "robotics",
        "archetype": "powered_exoskeleton",
        "objective": "Determine whether a human-powered exoskeleton concept is technically feasible.",
        "facts": {
            "use_case": "human augmentation",
            "target": "wearable system",
        },
        "factors": [
            ("power_density", "energy", True, 0.99, 0.94),
            ("actuator_torque_density", "mechanical", True, 0.96, 0.88),
            ("system_mass", "mechanical", True, 0.94, 0.81),
            ("thermal_management", "thermal", True, 0.90, 0.87),
            ("human_safety", "safety", True, 0.99, 0.92),
            ("exoskeleton_color", "appearance", False, 0.00, 0.01),
        ],
    },
    {
        "case_id": "manufacturing_001",
        "domain": "business",
        "industry": "manufacturing",
        "archetype": "new_factory",
        "objective": "Determine whether a proposed manufacturing operation is economically viable.",
        "facts": {
            "product": "industrial component",
            "market": "B2B",
        },
        "factors": [
            ("unit_production_cost", "economics", True, 0.97, 0.81),
            ("capacity_utilization", "operations", True, 0.94, 0.84),
            ("raw_material_cost", "supply_chain", True, 0.93, 0.76),
            ("customer_demand", "market", True, 0.96, 0.80),
            ("quality_failure_rate", "operations", True, 0.91, 0.73),
            ("factory_wall_color", "irrelevant", False, 0.00, 0.01),
        ],
    },
    {
        "case_id": "energy_001",
        "domain": "engineering",
        "industry": "energy",
        "archetype": "distributed_energy_system",
        "objective": "Determine whether a distributed renewable energy system is technically and economically viable.",
        "facts": {
            "system": "distributed generation",
            "target": "local users",
        },
        "factors": [
            ("energy_resource_availability", "resource", True, 0.95, 0.78),
            ("system_efficiency", "engineering", True, 0.93, 0.72),
            ("storage_requirement", "engineering", True, 0.91, 0.85),
            ("capital_cost", "economics", True, 0.96, 0.81),
            ("grid_reliability", "infrastructure", True, 0.88, 0.74),
            ("enclosure_color", "appearance", False, 0.00, 0.01),
        ],
    },
]


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    records = []

    for case in CASES:
        for (
            factor_id,
            category,
            relevant,
            importance,
            uncertainty,
        ) in case["factors"]:
            records.append(
                {
                    "case_id": case["case_id"],
                    "case_state": {
                        "domain": case["domain"],
                        "industry": case["industry"],
                        "archetype": case["archetype"],
                        "objective": case["objective"],
                        "facts": case["facts"],
                    },
                    "factor": {
                        "factor_id": factor_id,
                        "name": factor_id.replace("_", " "),
                        "category": category,
                    },
                    "labels": {
                        "relevant": relevant,
                        "importance": importance,
                        "uncertainty": uncertainty,
                    },
                    "metadata": {
                        "annotation_type": "expert_bootstrap",
                        "source": "initial_factor_corpus",
                    },
                }
            )

    with OUTPUT.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} examples to {OUTPUT}")
    print(f"Cases: {len(CASES)}")


if __name__ == "__main__":
    build()
