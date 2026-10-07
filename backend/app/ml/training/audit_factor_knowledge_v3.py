from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("data/training/factor_corpus")
CORPUS = ROOT / "factor_knowledge_v3.jsonl"
PAIRS = ROOT / "factor_pairs_v3.jsonl"


def load(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def main():
    records = load(CORPUS)
    pairs = load(PAIRS)

    by_case = defaultdict(list)

    for r in records:
        by_case[r["case_id"]].append(r)

    domains = Counter()
    industries = Counter()
    categories = Counter()
    positives = 0
    negatives = 0

    for r in records:
        state = r["case_state"]
        factor = r["factor"]

        domains[state["domain"]] += 1
        industries[state["industry"]] += 1
        categories[factor["category"]] += 1

        if r["labels"]["relevant"]:
            positives += 1
        else:
            negatives += 1

    margins = [
        p["importance_margin"]
        for p in pairs
    ]

    hard = sum(m >= 0.05 for m in margins)
    medium = sum(m >= 0.10 for m in margins)
    strong = sum(m >= 0.20 for m in margins)
    very_strong = sum(m >= 0.30 for m in margins)

    duplicate_names = Counter(
        r["factor"]["name"]
        for r in records
    )

    print("=== FACTOR KNOWLEDGE V3 AUDIT ===")
    print()
    print("Cases:", len(by_case))
    print("Records:", len(records))
    print("Pairs:", len(pairs))
    print()

    print("=== LABEL BALANCE ===")
    print("Relevant:", positives)
    print("Irrelevant:", negatives)
    print(
        "Positive ratio:",
        round(positives / len(records), 4)
    )
    print()

    print("=== DOMAINS ===")
    for k, v in sorted(domains.items()):
        print(f"{k:20} {v}")
    print()

    print("=== INDUSTRIES ===")
    for k, v in sorted(industries.items()):
        print(f"{k:25} {v}")
    print()

    print("=== FACTOR CATEGORIES ===")
    for k, v in sorted(categories.items()):
        print(f"{k:25} {v}")
    print()

    print("=== PAIR MARGINS ===")
    print(">= 0.05:", hard)
    print(">= 0.10:", medium)
    print(">= 0.20:", strong)
    print(">= 0.30:", very_strong)
    print(
        "Mean:",
        round(sum(margins) / len(margins), 4)
    )
    print()

    print("=== CASE SIZES ===")
    for case_id, rs in sorted(by_case.items()):
        relevant = sum(
            r["labels"]["relevant"]
            for r in rs
        )

        print(
            f"{case_id:35} "
            f"factors={len(rs):2} "
            f"relevant={relevant:2}"
        )

    print()

    print("=== MOST REUSED FACTORS ===")
    for name, count in duplicate_names.most_common(20):
        print(f"{name:35} {count}")

    print()

    # Detect silly negatives.
    suspicious_terms = [
        "wall",
        "paint",
        "color",
        "colour",
        "font",
        "logo",
        "icon",
        "furniture",
        "lighting",
    ]

    suspicious = []

    for r in records:
        if not r["labels"]["relevant"]:
            name = r["factor"]["name"].lower()

            if any(
                term in name
                for term in suspicious_terms
            ):
                suspicious.append(
                    (r["case_id"], name)
                )

    print("=== NEGATIVE QUALITY ===")
    print(
        "Appearance/presentation negatives:",
        len(suspicious),
    )

    if suspicious:
        for case_id, name in suspicious:
            print(" ", case_id, "->", name)

    print()
    print("=== AUDIT COMPLETE ===")


if __name__ == "__main__":
    main()
