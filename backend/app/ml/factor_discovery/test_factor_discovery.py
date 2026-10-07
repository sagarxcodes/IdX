from app.ml.factor_discovery.service import (
    FactorDiscoveryService,
)


def main():

    service = FactorDiscoveryService(
        corpus_path=(
            "data/training/factor_corpus/factors.jsonl"
        ),
        checkpoint_dir=(
            "data/training/models/"
            "factor-discovery-v0-bootstrap"
        ),
    )

    case = {
        "domain": "business",
        "industry": "hospitality",
        "archetype": "new_hotel",
        "objective": (
            "Determine whether a 60-room hotel "
            "near an international airport can "
            "achieve sustainable profitability."
        ),
        "facts": {
            "location": "airport-adjacent",
            "rooms": 60,
            "target_customer": (
                "international business travelers"
            ),
        },
    }

    results = service.discover(case)

    print()
    print("=== IdX FACTOR DISCOVERY ===")
    print(
        f"Candidates evaluated: {len(results)}"
    )

    for index, factor in enumerate(
        results[:10],
        start=1,
    ):
        print(
            f"{index:02d}. "
            f"{factor['name']:<32} "
            f"retrieval={factor['retrieval_score']:.3f} "
            f"relevance={factor['relevance']:.3f} "
            f"importance={factor['importance']:.3f}"
        )


if __name__ == "__main__":
    main()
