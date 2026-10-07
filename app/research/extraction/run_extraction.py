from __future__ import annotations

import glob
import json
from pathlib import Path

from app.research.extraction.paper_processor import (
    ResearchExtractionModel,
    save_result,
)


ROOT = Path(__file__).resolve().parents[3]

NORMALIZED_DIR = ROOT / "data/research/papers/normalized"
CLAIMS_DIR = ROOT / "data/research/claims"
FACTORS_DIR = ROOT / "data/research/factors"
RELATIONSHIPS_DIR = ROOT / "data/research/relationships"

OUTPUT_DIR = ROOT / "data/research/extraction_runs"


def load_latest_papers():
    files = sorted(NORMALIZED_DIR.glob("openalex_*.jsonl"))

    if not files:
        raise FileNotFoundError(
            "No normalized OpenAlex corpus found."
        )

    path = files[-1]

    papers = []

    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                papers.append(json.loads(line))

    return path, papers


def main():
    path, papers = load_latest_papers()

    print("=== IdX RESEARCH EXTRACTION ===")
    print(f"Input: {path}")
    print(f"Papers: {len(papers)}")
    print()

    model = ResearchExtractionModel()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = []

    for index, paper in enumerate(papers, start=1):
        paper_id = paper.get("paper_id", "")

        print(
            f"[{index}/{len(papers)}] "
            f"{paper.get('title', '')[:100]}"
        )

        try:
            result = model.extract(paper)

            save_result(
                result,
                CLAIMS_DIR,
                FACTORS_DIR,
                RELATIONSHIPS_DIR,
            )

            summary.append(
                {
                    "paper_id": paper_id,
                    "status": "success",
                    "claims": len(result.claims),
                    "factors": len(result.factors),
                    "relationships": len(result.relationships),
                    "conditions": len(result.conditions),
                }
            )

            print(
                f"  claims={len(result.claims)} "
                f"factors={len(result.factors)} "
                f"relationships={len(result.relationships)} "
                f"conditions={len(result.conditions)}"
            )

        except Exception as exc:
            print(f"  ERROR: {exc}")

            summary.append(
                {
                    "paper_id": paper_id,
                    "status": "error",
                    "error": str(exc),
                }
            )

    summary_path = OUTPUT_DIR / "extraction_summary.json"

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    successful = sum(
        1 for item in summary
        if item["status"] == "success"
    )

    print()
    print("=== EXTRACTION COMPLETE ===")
    print(f"Successful: {successful}/{len(papers)}")
    print(f"Summary:   {summary_path}")


if __name__ == "__main__":
    main()
