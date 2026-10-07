from __future__ import annotations

import json
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote

import httpx

from app.research.schema import ResearchSource


OPENALEX_API = "https://api.openalex.org/works"

ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = ROOT / "data/research/papers/raw"
NORMALIZED_DIR = ROOT / "data/research/papers/normalized"


class OpenAlexClient:
    def __init__(
        self,
        mailto: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.mailto = mailto
        self.timeout = timeout

    def search(
        self,
        query: str,
        per_page: int = 25,
        pages: int = 1,
        open_access_only: bool = True,
    ) -> List[Dict]:
        results: List[Dict] = []

        for page in range(1, pages + 1):
            params = {
                "search": query,
                "per-page": min(per_page, 200),
                "page": page,
            }

            if open_access_only:
                params["filter"] = "open_access.is_oa:true"

            if self.mailto:
                params["mailto"] = self.mailto

            response = httpx.get(
                OPENALEX_API,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()

            payload = response.json()
            results.extend(payload.get("results", []))

            if len(payload.get("results", [])) < per_page:
                break

            time.sleep(0.2)

        return results


def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return ""

    positions = []

    for word, indexes in inverted_index.items():
        for index in indexes:
            positions.append((index, word))

    positions.sort()
    return " ".join(word for _, word in positions)


def normalize_work(work: Dict) -> Dict:
    primary_location = work.get("primary_location") or {}
    open_access = work.get("open_access") or {}

    authors = []

    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}

        if author.get("display_name"):
            authors.append(
                {
                    "id": author.get("id"),
                    "name": author.get("display_name"),
                }
            )

    topics = []

    for topic in work.get("topics") or []:
        topics.append(
            {
                "id": topic.get("id"),
                "name": topic.get("display_name"),
                "score": topic.get("score"),
            }
        )

    return {
        "source_id": "openalex",
        "paper_id": work.get("id"),
        "doi": work.get("doi"),
        "title": work.get("title") or "",
        "publication_year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "type": work.get("type"),
        "language": work.get("language"),
        "authors": authors,
        "topics": topics,
        "concepts": [
            {
                "id": c.get("id"),
                "name": c.get("display_name"),
                "score": c.get("score"),
            }
            for c in (work.get("concepts") or [])
        ],
        "abstract": reconstruct_abstract(
            work.get("abstract_inverted_index")
        ),
        "cited_by_count": work.get("cited_by_count", 0),
        "referenced_works_count": len(
            work.get("referenced_works") or []
        ),
        "open_access": {
            "is_oa": open_access.get("is_oa", False),
            "oa_status": open_access.get("oa_status"),
            "oa_url": open_access.get("oa_url"),
        },
        "primary_location": {
            "landing_page_url": primary_location.get(
                "landing_page_url"
            ),
            "pdf_url": primary_location.get("pdf_url"),
            "is_oa": primary_location.get("is_oa", False),
        },
        "retrieved_at": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(),
        ),
    }


def deduplicate(works: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []

    for work in works:
        key = (
            work.get("doi")
            or work.get("paper_id")
            or work.get("title", "").strip().lower()
        )

        if not key or key in seen:
            continue

        seen.add(key)
        unique.append(work)

    return unique


def save_jsonl(path: Path, records: List[Dict]):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(
                json.dumps(record, ensure_ascii=False)
                + "\n"
            )


def acquire(
    queries: List[str],
    per_query: int = 25,
    pages: int = 1,
):
    client = OpenAlexClient()

    discovered = []

    for query in queries:
        print(f"[SEARCH] {query}")

        works = client.search(
            query=query,
            per_page=per_query,
            pages=pages,
            open_access_only=True,
        )

        print(f"  discovered={len(works)}")

        for work in works:
            raw = dict(work)
            raw["_idx_query"] = query
            discovered.append(raw)

    unique = deduplicate(discovered)

    normalized = [
        normalize_work(work)
        for work in unique
    ]

    timestamp = time.strftime(
        "%Y%m%d_%H%M%S",
        time.gmtime(),
    )

    raw_path = RAW_DIR / f"openalex_{timestamp}.jsonl"
    normalized_path = (
        NORMALIZED_DIR
        / f"openalex_{timestamp}.jsonl"
    )

    save_jsonl(raw_path, discovered)
    save_jsonl(normalized_path, normalized)

    print()
    print("=== OPENALEX ACQUISITION ===")
    print(f"Raw records:        {len(discovered)}")
    print(f"Unique papers:      {len(unique)}")
    print(f"Normalized papers:  {len(normalized)}")
    print(f"Raw:                {raw_path}")
    print(f"Normalized:         {normalized_path}")


if __name__ == "__main__":
    acquire(
        queries=[
            "business strategy competitive advantage",
            "firm performance productivity",
            "market demand customer behavior",
            "technology adoption innovation",
            "operational efficiency supply chain",
            "business risk regulation",
        ],
        per_query=20,
        pages=1,
    )
