from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[4]

# The retrieval algorithm is domain-independent.
# A corpus can be selected through IDX_RESEARCH_CORPUS so the same
# investigation engine can operate on different evidence collections.
#
# Example:
#   IDX_RESEARCH_CORPUS=data/research/papers/normalized/education_openalex_demo_v2.jsonl
#
# If no corpus is configured, the original general research corpus is used.
DEFAULT_CORPUS = (
    PROJECT_ROOT
    / "data/research/papers/normalized/openalex_20261006_173151.jsonl"
)

CORPUS = Path(
    __import__("os").environ.get(
        "IDX_RESEARCH_CORPUS",
        str(DEFAULT_CORPUS),
    )
)

if not CORPUS.is_absolute():
    CORPUS = PROJECT_ROOT / CORPUS

# Generic words that create noisy matches across almost every business paper.
STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "are", "was",
    "were", "have", "has", "had", "into", "their", "there", "about",
    "what", "when", "where", "which", "while", "through", "between",
    "than", "then", "they", "them", "these", "those", "will", "would",
    "could", "should", "can", "our", "your", "you", "its", "not",
    "but", "also", "how", "why", "who", "all", "any", "some",
    "want", "understand", "need", "open", "make", "get", "use",
    "business", "company", "companies", "firm", "firms",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def _paper_text(paper: Dict[str, Any]) -> str:
    parts = [
        paper.get("title", ""),
        paper.get("abstract", ""),
    ]

    for topic in paper.get("topics", []) or []:
        if isinstance(topic, dict):
            parts.extend(
                [
                    str(topic.get("display_name", "")),
                    str(topic.get("subfield", "")),
                    str(topic.get("field", "")),
                ]
            )
        else:
            parts.append(str(topic))

    for concept in paper.get("concepts", []) or []:
        if isinstance(concept, dict):
            parts.append(str(concept.get("display_name", "")))
        else:
            parts.append(str(concept))

    return " ".join(parts)


def _domain_terms(query: str) -> set[str]:
    """
    Small transparent domain vocabulary.
    This is retrieval weighting, NOT a domain-specific question flow.
    """
    q = query.lower()

    vocabulary = {
        "hotel": {
            "hotel", "hospitality", "lodging", "accommodation",
            "tourism", "occupancy", "room", "rooms", "guest",
            "booking", "pricing", "demand", "competition",
        },
        "restaurant": {
            "restaurant", "food", "dining", "menu", "customer",
            "pricing", "demand", "location",
        },
        "retail": {
            "retail", "store", "shop", "inventory", "customer",
            "pricing", "demand", "sales",
        },
        "agriculture": {
            "farm", "farmer", "crop", "soil", "irrigation",
            "agriculture", "yield", "fertilizer", "weather",
        },
        "technology": {
            "software", "technology", "platform", "ai", "machine",
            "learning", "adoption", "users", "product",
        },
    }

    terms = set()

    for group in vocabulary.values():
        if any(term in q for term in group):
            terms.update(group & _tokens(q))

    return terms


def retrieve_research_evidence(
    query: str,
    limit: int = 3,
) -> List[Dict[str, Any]]:
    if not CORPUS.exists():
        return []

    query_tokens = _tokens(query)

    if not query_tokens:
        return []

    domain_terms = _domain_terms(query)
    results = []

    with CORPUS.open() as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            try:
                paper = json.loads(line)
            except json.JSONDecodeError:
                continue

            title = paper.get("title", "")
            abstract = paper.get("abstract", "")

            title_tokens = _tokens(title)
            abstract_tokens = _tokens(abstract)
            paper_tokens = _tokens(_paper_text(paper))

            title_overlap = query_tokens & title_tokens
            abstract_overlap = query_tokens & abstract_tokens
            domain_overlap = domain_terms & paper_tokens

            # Ignore papers that only match generic/weak vocabulary.
            if not title_overlap and not domain_overlap and len(abstract_overlap) < 2:
                continue

            # Transparent lexical scoring:
            #
            # title/domain matches matter more than generic abstract overlap.
            title_score = (
                len(title_overlap) / max(len(query_tokens), 1)
            )
            abstract_score = (
                len(abstract_overlap) / max(len(query_tokens), 1)
            )
            domain_score = (
                len(domain_overlap) / max(len(domain_terms), 1)
                if domain_terms
                else 0.0
            )

            score = (
                0.50 * title_score
                + 0.25 * abstract_score
                + 0.25 * domain_score
            )

            if score <= 0:
                continue

            results.append((score, paper))

    results.sort(
        key=lambda item: (
            item[0],
            item[1].get("cited_by_count", 0),
        ),
        reverse=True,
    )

    evidence = []

    for score, paper in results[:limit]:
        evidence.append(
            {
                "evidence_id": f"research_{paper.get('paper_id')}",
                "source_id": paper.get("source_id", "openalex"),
                "source_type": "research_paper",
                "title": paper.get("title", ""),
                "claim": paper.get("abstract", ""),
                "source_url": (
                    paper.get("doi")
                    or (
                        paper.get("primary_location", {})
                        or {}
                    ).get("landing_page_url")
                ),
                "published_at": paper.get("publication_date"),
                "relevance": round(min(score, 1.0), 4),
                "confidence": 0.0,
                "retrieval_method": "lexical_baseline_weighted",
                "status": "research_source_not_claim",
                "paper_id": paper.get("paper_id"),
                "doi": paper.get("doi"),
                "cited_by_count": paper.get("cited_by_count", 0),
            }
        )

    return evidence
