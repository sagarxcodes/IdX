import json
from pathlib import Path

from app.research.extraction.paper_processor import ResearchExtractionModel


ROOT = Path.cwd()

files = sorted(
    (ROOT / "data/research/papers/normalized").glob("openalex_*.jsonl")
)

if not files:
    raise FileNotFoundError("No normalized OpenAlex corpus found.")

path = files[-1]

with path.open(encoding="utf-8") as f:
    papers = [
        json.loads(line)
        for line in f
        if line.strip()
    ]

print("=== IdX RESEARCH EXTRACTION PILOT ===")
print(f"Corpus: {path}")
print(f"Available papers: {len(papers)}")

model = ResearchExtractionModel()

for i, paper in enumerate(papers[:5], 1):
    print("\n" + "=" * 80)
    print(f"PAPER {i}")
    print(f"TITLE: {paper.get('title', '')}")
    print("=" * 80)

    result = model.extract(paper)

    print("\nCLAIMS:")
    for claim in result.claims:
        print(" -", claim.get("text"))

    print("\nFACTORS:")
    for factor in result.factors:
        print(
            " -",
            factor.get("name"),
            "| category:",
            factor.get("category"),
        )

    print("\nRELATIONSHIPS:")
    for rel in result.relationships:
        print(
            " -",
            rel.get("source_factor"),
            "->",
            rel.get("target_factor"),
            f"[{rel.get('relation')}]",
        )

    print("\nCONDITIONS:")
    for condition in result.conditions:
        print(" -", condition.get("description"))

    print("\nLIMITATIONS:")
    for limitation in result.limitations:
        print(" -", limitation)

print("\n=== PILOT COMPLETE ===")
