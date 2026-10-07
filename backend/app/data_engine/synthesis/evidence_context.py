from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class EvidenceContext:
    """
    Grounded context assembled from retrieved evidence.

    This layer does not generate claims or conclusions.
    It preserves provenance so downstream reasoning can distinguish
    research evidence, discussions, datasets, and other sources.
    """

    query: str
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    context_text: str = ""
    source_types: List[str] = field(default_factory=list)
    evidence_count: int = 0


class EvidenceContextBuilder:
    """
    Converts heterogeneous retrieved evidence into a bounded context
    suitable for downstream reasoning and question selection.
    """

    def __init__(self, max_items: int = 8, max_chars: int = 12000) -> None:
        self.max_items = max_items
        self.max_chars = max_chars

    def build(
        self,
        query: str,
        evidence: List[Dict[str, Any]],
    ) -> EvidenceContext:
        selected = evidence[: self.max_items]

        blocks: List[str] = []
        source_types: List[str] = []

        for index, item in enumerate(selected, start=1):
            source_type = str(item.get("source_type", "unknown"))
            title = str(item.get("title", "")).strip()
            claim = str(item.get("claim", "")).strip()
            source_id = str(
                item.get("source_id")
                or item.get("paper_id")
                or item.get("evidence_id")
                or f"evidence_{index}"
            )

            if source_type not in source_types:
                source_types.append(source_type)

            block = (
                f"[Evidence {index}]\n"
                f"source_type: {source_type}\n"
                f"source_id: {source_id}\n"
            )

            if title:
                block += f"title: {title}\n"

            if claim:
                block += f"content: {claim}\n"

            relevance = item.get("relevance")
            if relevance is not None:
                block += f"relevance: {relevance}\n"

            block += f"verification_status: {item.get('status', 'unknown')}"

            blocks.append(block)

        context_text = "\n\n".join(blocks)

        if len(context_text) > self.max_chars:
            context_text = context_text[: self.max_chars].rstrip() + "\n[context truncated]"

        return EvidenceContext(
            query=query,
            evidence=selected,
            context_text=context_text,
            source_types=source_types,
            evidence_count=len(selected),
        )


evidence_context_builder = EvidenceContextBuilder()
