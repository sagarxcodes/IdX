from __future__ import annotations

import json
from pathlib import Path


OUT = Path(
    "data/training/factor_corpus/"
    "factor_knowledge_v2.jsonl"
)


CASES = [
    {
        "case_id": "hotel_airport_001",
        "case_state": {
            "domain": "business",
            "industry": "hospitality",
            "archetype": "new_hotel",
            "objective": (
                "Evaluate commercial viability of a premium "
                "airport hotel."
            ),
            "facts": {
                "location": "near international airport",
                "target_customer": "business travelers",
                "price_segment": "premium",
                "rooms": 60,
            },
        },
        "factors": [
            {
                "id": "corporate_booking_demand",
                "category": "customer",
                "importance": 0.96,
                "uncertainty": 0.91,
                "relevant": True,
                "reason": (
                    "The stated target customer is business travelers, "
                    "so corporate demand directly affects occupancy."
                ),
                "evidence": [
                    "corporate travel volume",
                    "corporate booking data",
                    "business traveler demand",
                ],
                "decision_impact": 0.96,
                "outcome_impact": 0.94,
            },
            {
                "id": "airport_business_travel_demand",
                "category": "market",
                "importance": 0.95,
                "uncertainty": 0.93,
                "relevant": True,
                "reason": (
                    "Airport proximity only creates value if sufficient "
                    "business and transit demand exists."
                ),
                "evidence": [
                    "airport passenger statistics",
                    "business travel statistics",
                    "local hotel demand",
                ],
                "decision_impact": 0.95,
                "outcome_impact": 0.92,
            },
            {
                "id": "competitor_room_rates",
                "category": "competition",
                "importance": 0.91,
                "uncertainty": 0.87,
                "relevant": True,
                "reason": (
                    "Comparable hotel pricing constrains achievable "
                    "room rates."
                ),
                "evidence": [
                    "competitor room rates",
                    "occupancy estimates",
                    "competitor positioning",
                ],
                "decision_impact": 0.90,
                "outcome_impact": 0.86,
            },
            {
                "id": "expected_occupancy",
                "category": "economics",
                "importance": 0.94,
                "uncertainty": 0.90,
                "relevant": True,
                "reason": (
                    "Occupancy is a major driver of hotel revenue "
                    "and break-even."
                ),
                "evidence": [
                    "comparable occupancy",
                    "historical local occupancy",
                    "seasonality data",
                ],
                "decision_impact": 0.97,
                "outcome_impact": 0.96,
            },
            {
                "id": "tourist_arrival_volume",
                "category": "market",
                "importance": 0.52,
                "uncertainty": 0.84,
                "relevant": True,
                "reason": (
                    "Tourist demand can contribute to occupancy, "
                    "but it is less aligned with the stated "
                    "business-traveler positioning."
                ),
                "evidence": [
                    "tourist arrival statistics",
                    "tourism seasonality",
                ],
                "decision_impact": 0.45,
                "outcome_impact": 0.41,
            },
            {
                "id": "operating_cost_per_room",
                "category": "economics",
                "importance": 0.88,
                "uncertainty": 0.82,
                "relevant": True,
                "reason": (
                    "Room-level operating cost affects contribution "
                    "margin and break-even occupancy."
                ),
                "evidence": [
                    "utility costs",
                    "staffing costs",
                    "housekeeping costs",
                    "maintenance costs",
                ],
                "decision_impact": 0.88,
                "outcome_impact": 0.87,
            },
            {
                "id": "hotel_logo_color",
                "category": "branding",
                "importance": 0.01,
                "uncertainty": 0.02,
                "relevant": False,
                "reason": "No material relationship to commercial viability.",
                "decision_impact": 0.0,
                "outcome_impact": 0.0,
            },
        ],
        "relationships": [
            {
                "source": "airport_business_travel_demand",
                "target": "corporate_booking_demand",
                "type": "supports",
                "weight": 0.82,
            },
            {
                "source": "corporate_booking_demand",
                "target": "expected_occupancy",
                "type": "influences",
                "weight": 0.84,
            },
            {
                "source": "competitor_room_rates",
                "target": "expected_occupancy",
                "type": "influences",
                "weight": 0.61,
            },
            {
                "source": "competitor_room_rates",
                "target": "achievable_room_price",
                "type": "constrains",
                "weight": 0.86,
            },
            {
                "source": "expected_occupancy",
                "target": "hotel_profitability",
                "type": "influences",
                "weight": 0.91,
            },
            {
                "source": "operating_cost_per_room",
                "target": "hotel_profitability",
                "type": "influences",
                "weight": 0.88,
            },
        ],
    },

    {
        "case_id": "hotel_tourist_001",
        "case_state": {
            "domain": "business",
            "industry": "hospitality",
            "archetype": "new_hotel",
            "objective": (
                "Evaluate commercial viability of a leisure hotel."
            ),
            "facts": {
                "location": "tourist destination",
                "target_customer": "leisure travelers",
                "price_segment": "mid-market",
            },
        },
        "factors": [
            {
                "id": "tourist_arrival_volume",
                "category": "market",
                "importance": 0.98,
                "uncertainty": 0.91,
                "relevant": True,
                "reason": (
                    "The hotel targets leisure travelers in a tourist "
                    "destination, making visitor volume central to demand."
                ),
                "evidence": [
                    "tourist arrivals",
                    "hotel demand",
                    "tourism statistics",
                ],
                "decision_impact": 0.97,
                "outcome_impact": 0.95,
            },
            {
                "id": "seasonal_demand",
                "category": "market",
                "importance": 0.96,
                "uncertainty": 0.93,
                "relevant": True,
                "reason": (
                    "Leisure destinations can have strong seasonal "
                    "variation affecting occupancy and cash flow."
                ),
                "evidence": [
                    "monthly tourist arrivals",
                    "historical hotel occupancy",
                    "seasonality",
                ],
                "decision_impact": 0.94,
                "outcome_impact": 0.92,
            },
            {
                "id": "corporate_booking_demand",
                "category": "customer",
                "importance": 0.31,
                "uncertainty": 0.86,
                "relevant": False,
                "reason": (
                    "Corporate demand may exist but is poorly aligned "
                    "with the stated leisure positioning."
                ),
                "evidence": [
                    "corporate travel volume",
                ],
                "decision_impact": 0.25,
                "outcome_impact": 0.22,
            },
            {
                "id": "local_attractions",
                "category": "market",
                "importance": 0.87,
                "uncertainty": 0.75,
                "relevant": True,
                "reason": (
                    "Attractions influence destination attractiveness "
                    "and leisure traveler demand."
                ),
                "evidence": [
                    "visitor statistics",
                    "attraction footfall",
                    "tourism surveys",
                ],
                "decision_impact": 0.82,
                "outcome_impact": 0.80,
            },
            {
                "id": "competitor_room_rates",
                "category": "competition",
                "importance": 0.90,
                "uncertainty": 0.85,
                "relevant": True,
                "reason": (
                    "Competitor pricing affects achievable pricing "
                    "and positioning."
                ),
                "evidence": [
                    "competitor rates",
                    "competitor occupancy",
                    "guest reviews",
                ],
                "decision_impact": 0.88,
                "outcome_impact": 0.84,
            },
            {
                "id": "weekend_occupancy",
                "category": "economics",
                "importance": 0.82,
                "uncertainty": 0.79,
                "relevant": True,
                "reason": (
                    "Weekend occupancy is particularly relevant for "
                    "a leisure-focused hotel."
                ),
                "evidence": [
                    "historical weekend occupancy",
                    "comparable hotel data",
                ],
                "decision_impact": 0.79,
                "outcome_impact": 0.76,
            },
        ],
        "relationships": [
            {
                "source": "tourist_arrival_volume",
                "target": "seasonal_demand",
                "type": "conditions",
                "weight": 0.78,
            },
            {
                "source": "seasonal_demand",
                "target": "weekend_occupancy",
                "type": "influences",
                "weight": 0.64,
            },
            {
                "source": "local_attractions",
                "target": "tourist_arrival_volume",
                "type": "supports",
                "weight": 0.58,
            },
        ],
    },

    {
        "case_id": "trading_signal_001",
        "case_state": {
            "domain": "finance",
            "industry": "financial_markets",
            "archetype": "systematic_trading_strategy",
            "objective": (
                "Determine whether a short-horizon market signal "
                "is economically exploitable."
            ),
            "facts": {
                "asset_class": "equities",
                "horizon": "short term",
                "execution": "automated",
            },
        },
        "factors": [
            {
                "id": "out_of_sample_predictive_power",
                "category": "research",
                "importance": 1.00,
                "uncertainty": 0.96,
                "relevant": True,
                "reason": (
                    "A signal without robust out-of-sample predictive "
                    "power has little evidence of exploitable edge."
                ),
                "evidence": [
                    "walk-forward tests",
                    "out-of-sample returns",
                    "statistical significance",
                ],
                "decision_impact": 0.99,
                "outcome_impact": 0.98,
            },
            {
                "id": "transaction_costs",
                "category": "execution",
                "importance": 0.99,
                "uncertainty": 0.89,
                "relevant": True,
                "reason": (
                    "Trading costs can eliminate an otherwise "
                    "statistically significant signal."
                ),
                "evidence": [
                    "broker costs",
                    "spread",
                    "slippage",
                    "market impact",
                ],
                "decision_impact": 0.97,
                "outcome_impact": 0.96,
            },
            {
                "id": "signal_decay",
                "category": "strategy",
                "importance": 0.97,
                "uncertainty": 0.94,
                "relevant": True,
                "reason": (
                    "Short-horizon signals may lose predictive power "
                    "quickly after discovery."
                ),
                "evidence": [
                    "signal half-life",
                    "performance by holding period",
                ],
                "decision_impact": 0.94,
                "outcome_impact": 0.93,
            },
            {
                "id": "liquidity",
                "category": "market",
                "importance": 0.95,
                "uncertainty": 0.82,
                "relevant": True,
                "reason": (
                    "Liquidity determines whether theoretical trades "
                    "can actually be executed at modeled prices."
                ),
                "evidence": [
                    "volume",
                    "bid-ask spread",
                    "market depth",
                ],
                "decision_impact": 0.91,
                "outcome_impact": 0.90,
            },
            {
                "id": "market_regime_stability",
                "category": "risk",
                "importance": 0.91,
                "uncertainty": 0.93,
                "relevant": True,
                "reason": (
                    "Signal behavior can change across market regimes."
                ),
                "evidence": [
                    "regime analysis",
                    "performance across historical regimes",
                ],
                "decision_impact": 0.90,
                "outcome_impact": 0.91,
            },
            {
                "id": "latency",
                "category": "execution",
                "importance": 0.84,
                "uncertainty": 0.80,
                "relevant": True,
                "reason": (
                    "For short-horizon automated execution, latency "
                    "can materially affect realized edge."
                ),
                "evidence": [
                    "execution latency",
                    "order timestamps",
                    "fill quality",
                ],
                "decision_impact": 0.82,
                "outcome_impact": 0.85,
            },
            {
                "id": "dashboard_font",
                "category": "presentation",
                "importance": 0.00,
                "uncertainty": 0.01,
                "relevant": False,
                "reason": "No material relationship to signal profitability.",
                "decision_impact": 0.0,
                "outcome_impact": 0.0,
            },
        ],
        "relationships": [
            {
                "source": "out_of_sample_predictive_power",
                "target": "signal_decay",
                "type": "must_be_tested_with",
                "weight": 0.81,
            },
            {
                "source": "transaction_costs",
                "target": "out_of_sample_predictive_power",
                "type": "constrains_realized_edge",
                "weight": 0.77,
            },
            {
                "source": "liquidity",
                "target": "transaction_costs",
                "type": "influences",
                "weight": 0.69,
            },
            {
                "source": "latency",
                "target": "realized_edge",
                "type": "influences",
                "weight": 0.74,
            },
        ],
    },
]


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    records = []

    for case in CASES:
        relationships = case.get("relationships", [])

        for factor in case["factors"]:
            records.append(
                {
                    "case_id": case["case_id"],
                    "case_state": case["case_state"],
                    "factor": {
                        "factor_id": factor["id"],
                        "name": factor["id"].replace("_", " "),
                        "category": factor["category"],
                    },
                    "labels": {
                        "relevant": factor["relevant"],
                        "importance": factor["importance"],
                        "uncertainty": factor["uncertainty"],
                        "decision_impact": factor["decision_impact"],
                        "outcome_impact": factor["outcome_impact"],
                    },
                    "relevance_reason": factor["reason"],
                    "evidence_requirements": factor.get(
                        "evidence",
                        []
                    ),
                    "relationships": [
                        r
                        for r in relationships
                        if (
                            r["source"] == factor["id"]
                            or r["target"] == factor["id"]
                        )
                    ],
                    "metadata": {
                        "annotation_type": "expert_bootstrap_v2",
                        "source": "factor_knowledge_corpus_v2",
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

    print("=== FACTOR KNOWLEDGE CORPUS V2 ===")
    print(f"Cases: {len(CASES)}")
    print(f"Records: {len(records)}")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    build()
