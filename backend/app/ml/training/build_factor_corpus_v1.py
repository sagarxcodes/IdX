from __future__ import annotations

import json
from pathlib import Path


OUT = Path("data/training/factor_corpus/factors_v1.jsonl")


CASES = [
    {
        "case_id": "hotel_airport_001",
        "domain": "business",
        "industry": "hospitality",
        "archetype": "new_hotel",
        "objective": "Evaluate commercial viability of a premium airport hotel.",
        "facts": {
            "location": "near international airport",
            "target_customer": "business travelers",
            "price_segment": "premium",
            "rooms": 60,
        },
        "factors": {
            "airport_business_travel_demand": ("market", 1.00, 0.95),
            "competitor_room_rates": ("competition", 0.98, 0.90),
            "corporate_booking_demand": ("customer", 0.96, 0.91),
            "expected_occupancy": ("economics", 0.99, 0.94),
            "seasonality": ("market", 0.82, 0.75),
            "operating_cost_per_room": ("economics", 0.91, 0.83),
            "logo_color": ("branding", 0.00, 0.05),
            "founder_favorite_food": ("irrelevant", 0.00, 0.01),
        },
    },
    {
        "case_id": "hotel_tourist_001",
        "domain": "business",
        "industry": "hospitality",
        "archetype": "new_hotel",
        "objective": "Evaluate commercial viability of a leisure hotel.",
        "facts": {
            "location": "tourist destination",
            "target_customer": "leisure travelers",
            "price_segment": "mid-market",
        },
        "factors": {
            "tourist_arrival_volume": ("market", 0.99, 0.88),
            "seasonal_demand": ("market", 0.97, 0.92),
            "local_attractions": ("market", 0.89, 0.73),
            "competitor_room_rates": ("competition", 0.93, 0.81),
            "weekend_occupancy": ("economics", 0.88, 0.76),
            "corporate_booking_demand": ("customer", 0.35, 0.84),
            "logo_color": ("branding", 0.00, 0.04),
        },
    },
    {
        "case_id": "saas_b2b_001",
        "domain": "business",
        "industry": "software",
        "archetype": "new_saas",
        "objective": "Determine whether a B2B SaaS product has a viable business model.",
        "facts": {
            "customer": "small businesses",
            "pricing": "subscription",
            "sales_model": "B2B",
        },
        "factors": {
            "customer_problem_severity": ("customer", 1.00, 0.93),
            "willingness_to_pay": ("customer", 0.99, 0.91),
            "customer_acquisition_cost": ("economics", 0.96, 0.89),
            "retention": ("customer", 0.98, 0.94),
            "competitor_differentiation": ("competition", 0.92, 0.87),
            "market_size": ("market", 0.90, 0.78),
            "founder_preferred_language": ("technology", 0.02, 0.10),
            "logo_animation": ("presentation", 0.00, 0.02),
        },
    },
    {
        "case_id": "saas_consumer_001",
        "domain": "business",
        "industry": "software",
        "archetype": "consumer_subscription",
        "objective": "Evaluate a consumer subscription software product.",
        "facts": {
            "customer": "individual consumers",
            "pricing": "monthly subscription",
        },
        "factors": {
            "consumer_conversion_rate": ("customer", 0.98, 0.90),
            "churn_rate": ("customer", 1.00, 0.95),
            "customer_acquisition_cost": ("economics", 0.97, 0.91),
            "price_sensitivity": ("customer", 0.95, 0.87),
            "viral_coefficient": ("growth", 0.84, 0.80),
            "enterprise_sales_cycle": ("sales", 0.12, 0.85),
            "founder_preferred_language": ("technology", 0.02, 0.08),
        },
    },
    {
        "case_id": "trading_signal_001",
        "domain": "finance",
        "industry": "financial_markets",
        "archetype": "systematic_trading_strategy",
        "objective": "Determine whether a short-horizon market signal is exploitable.",
        "facts": {
            "asset_class": "equities",
            "horizon": "short term",
            "execution": "automated",
        },
        "factors": {
            "out_of_sample_predictive_power": ("research", 1.00, 0.96),
            "transaction_costs": ("execution", 0.99, 0.88),
            "signal_decay": ("strategy", 0.98, 0.94),
            "liquidity": ("market", 0.96, 0.79),
            "market_regime_stability": ("risk", 0.92, 0.93),
            "latency": ("execution", 0.85, 0.82),
            "dashboard_font": ("presentation", 0.00, 0.01),
            "office_location": ("operations", 0.02, 0.30),
        },
    },
    {
        "case_id": "agri_crop_001",
        "domain": "agriculture",
        "industry": "crop_production",
        "archetype": "commercial_farm",
        "objective": "Select an economically suitable crop strategy.",
        "facts": {
            "farm_size": "2.5 acres",
            "region": "South India",
            "goal": "maximize risk-adjusted return",
        },
        "factors": {
            "soil_conditions": ("production", 0.98, 0.85),
            "water_availability": ("resources", 1.00, 0.91),
            "expected_yield": ("production", 0.98, 0.90),
            "market_price": ("market", 0.97, 0.87),
            "weather_risk": ("risk", 0.96, 0.94),
            "crop_duration": ("production", 0.91, 0.82),
            "farmer_favorite_color": ("irrelevant", 0.00, 0.01),
        },
    },
    {
        "case_id": "robotics_exoskeleton_001",
        "domain": "engineering",
        "industry": "robotics",
        "archetype": "powered_exoskeleton",
        "objective": "Determine technical feasibility of a wearable powered exoskeleton.",
        "facts": {
            "use_case": "human augmentation",
            "constraint": "wearable",
        },
        "factors": {
            "power_density": ("energy", 1.00, 0.97),
            "actuator_torque_density": ("mechanical", 0.99, 0.91),
            "system_mass": ("mechanical", 0.96, 0.84),
            "thermal_management": ("thermal", 0.94, 0.90),
            "human_safety": ("safety", 1.00, 0.96),
            "battery_energy_density": ("energy", 0.98, 0.94),
            "paint_color": ("appearance", 0.00, 0.01),
        },
    },
    {
        "case_id": "manufacturing_001",
        "domain": "business",
        "industry": "manufacturing",
        "archetype": "new_factory",
        "objective": "Determine whether a new manufacturing operation is economically viable.",
        "facts": {
            "product": "industrial component",
            "customer": "B2B",
        },
        "factors": {
            "customer_demand": ("market", 0.98, 0.86),
            "unit_production_cost": ("economics", 1.00, 0.91),
            "capacity_utilization": ("operations", 0.96, 0.88),
            "raw_material_cost": ("supply_chain", 0.95, 0.84),
            "quality_failure_rate": ("operations", 0.92, 0.80),
            "supply_chain_reliability": ("supply_chain", 0.89, 0.83),
            "factory_wall_color": ("appearance", 0.00, 0.01),
        },
    },
    {
        "case_id": "energy_microgrid_001",
        "domain": "engineering",
        "industry": "energy",
        "archetype": "distributed_microgrid",
        "objective": "Evaluate technical and economic viability of a renewable microgrid.",
        "facts": {
            "generation": "renewable",
            "system": "distributed",
        },
        "factors": {
            "renewable_resource_availability": ("resource", 0.98, 0.84),
            "load_profile": ("demand", 0.96, 0.88),
            "storage_requirement": ("engineering", 0.97, 0.93),
            "system_efficiency": ("engineering", 0.94, 0.78),
            "capital_cost": ("economics", 0.99, 0.87),
            "grid_reliability": ("infrastructure", 0.91, 0.76),
            "enclosure_color": ("appearance", 0.00, 0.01),
        },
    },
]


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    records = []

    for case in CASES:
        for factor_id, values in case["factors"].items():
            category, importance, uncertainty = values

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
                        "relevant": importance >= 0.50,
                        "importance": importance,
                        "uncertainty": uncertainty,
                    },
                    "metadata": {
                        "annotation_type": "expert_bootstrap",
                        "source": "factor_corpus_v1",
                    },
                }
            )

    with OUT.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print("=== FACTOR CORPUS V1 ===")
    print(f"Cases:   {len(CASES)}")
    print(f"Records: {len(records)}")
    print(f"Output:  {OUT}")


if __name__ == "__main__":
    build()
