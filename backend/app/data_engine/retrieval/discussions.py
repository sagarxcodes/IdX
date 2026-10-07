from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[4]

CORPUS = PROJECT_ROOT / "data/demo/education_discussions.jsonl"

STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "are", "was",
    "were", "have", "has", "had", "into", "their", "there", "about",
    "what", "when", "where", "which", "while", "through", "between",
    "than", "then", "they", "them", "these", "those", "will", "would",
    "could", "should", "can", "our", "your", "you", "its", "not",
    "but", "also", "how", "why", "who", "all", "any", "some",
    "want", "understand", "need", "make", "get", "use",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", text.lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def retrieve_discussion_evidence(
    query: str,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    if not CORPUS.exists():
        return []

    query_tokens = _tokens(query)

    if not query_tokens:
        return []

    results = []

    with CORPUS.open() as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            text = item.get("text", "")
            overlap = query_tokens & _tokens(text)

            if not overlap:
                continue

            relevance = len(overlap) / max(len(query_tokens), 1)

            results.append({
                "evidence_id": item.get("evidence_id"),
                "source_id": item.get("source_id"),
                "source_type": "discussion",
                "title": "Curated discussion",
                "claim": text,
                "source_url": None,
                "published_at": item.get("timestamp"),
                "relevance": round(min(relevance, 1.0), 4),
                "confidence": 0.0,
                "retrieval_method": "lexical_discussion_baseline",
                "status": "signal_not_verified_fact",
                "platform": item.get("platform", "unknown"),
            })

    results.sort(
        key=lambda item: item["relevance"],
        reverse=True,
    )

    return results[:limit]
