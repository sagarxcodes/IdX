import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data/research/sources/registry_v1.json"


SOURCES = [
    {
        "source_id": "world_bank_enterprise_surveys",
        "name": "World Bank Enterprise Surveys",
        "source_type": "firm_level_dataset",
        "url": "https://www.enterprisesurveys.org/",
        "coverage": [
            "finance",
            "infrastructure",
            "competition",
            "regulation",
            "innovation",
            "labor",
            "firm_performance",
        ],
        "geography": "global",
    },
    {
        "source_id": "oecd_productivity",
        "name": "OECD Productivity Statistics",
        "source_type": "official_statistics",
        "url": "https://www.oecd.org/en/data/indicators/productivity-levels.html",
        "coverage": [
            "labor_productivity",
            "multifactor_productivity",
            "capital",
            "industry",
            "firm_size",
        ],
        "geography": "international",
    },
    {
        "source_id": "fao_statistics",
        "name": "FAOSTAT",
        "source_type": "official_statistics",
        "url": "https://www.fao.org/faostat/",
        "coverage": [
            "agriculture",
            "production",
            "prices",
            "trade",
            "land",
            "inputs",
            "food_security",
        ],
        "geography": "global",
    },
    {
        "source_id": "openalex",
        "name": "OpenAlex",
        "source_type": "scholarly_graph",
        "url": "https://openalex.org/",
        "coverage": [
            "papers",
            "authors",
            "institutions",
            "topics",
            "citations",
            "open_access",
        ],
        "geography": "global",
    },
    {
        "source_id": "crossref",
        "name": "Crossref",
        "source_type": "scholarly_metadata",
        "url": "https://www.crossref.org/",
        "coverage": [
            "papers",
            "doi",
            "authors",
            "funding",
            "licenses",
            "updates",
        ],
        "geography": "global",
    },
    {
        "source_id": "semantic_scholar",
        "name": "Semantic Scholar",
        "source_type": "scholarly_graph",
        "url": "https://www.semanticscholar.org/",
        "coverage": [
            "papers",
            "citations",
            "authors",
            "references",
            "open_access",
            "datasets",
        ],
        "geography": "global",
    },
]


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(SOURCES, indent=2),
        encoding="utf-8",
    )

    print(f"Registered sources: {len(SOURCES)}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
