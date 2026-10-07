from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


@dataclass
class ExtractionResult:
    paper_id: str
    source_id: str
    claims: List[Dict[str, Any]]
    factors: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    conditions: List[Dict[str, Any]]
    limitations: List[str]
    raw_model_output: str


class ResearchExtractionModel:
    """
    Model-based research extraction.

    No sector-specific factor lists are used here.
    The model must infer factors and relationships from the supplied paper.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.device = (
            torch.device("mps")
            if torch.backends.mps.is_available()
            else torch.device("cpu")
        )

        self.model_name = model_name

        print(f"Loading extraction model: {model_name}")
        print(f"Device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float16 if self.device.type == "mps" else torch.float32,
        ).to(self.device)

        self.model.eval()

    def _prompt(self, paper: Dict[str, Any]) -> str:
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        year = paper.get("publication_year", "")
        topics = [
            t.get("name", "")
            for t in paper.get("topics", [])
            if t.get("name")
        ]

        return f"""
You are a scientific research analysis system.

Analyze the research paper below.

Your task is NOT to summarize it generally.
Extract structured knowledge that can later be used by a
decision-intelligence system.

Paper title:
{title}

Publication year:
{year}

Research topics:
{", ".join(topics)}

Abstract:
{abstract}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "claims": [
    {{
      "text": "specific empirical or theoretical finding",
      "claim_type": "finding|association|causal|mechanism|prediction|benchmark|limitation",
      "factors": ["factor names explicitly supported by the paper"],
      "direction": "positive|negative|mixed|none|unknown",
      "effect_size": null,
      "effect_unit": "",
      "confidence": 0.0,
      "evidence_strength": 0.0,
      "conditions": ["conditions under which the claim applies"],
      "limitations": ["limitations affecting interpretation"]
    }}
  ],
  "factors": [
    {{
      "name": "canonical factor",
      "category": "research-derived category",
      "description": "what the factor means in this study",
      "measurable_variables": ["variables used to measure it"]
    }}
  ],
  "relationships": [
    {{
      "source_factor": "factor",
      "target_factor": "factor",
      "relation": "increases|decreases|influences|mediates|moderates|correlates_with|constrains|depends_on",
      "direction": "positive|negative|mixed|unknown",
      "conditions": ["conditions"]
    }}
  ],
  "conditions": [
    {{
      "description": "contextual condition",
      "factors": ["affected factors"],
      "importance": 0.0
    }}
  ],
  "limitations": [
    "important study limitation"
  ]
}}

Rules:

1. Do not invent findings.
2. Do not infer a causal relationship unless the paper supports causality.
3. Distinguish correlation/association from causation.
4. Factors must represent meaningful variables, mechanisms,
   constraints, resources, behaviors, outcomes, or drivers.
5. Do not extract cosmetic or irrelevant details.
6. Preserve uncertainty.
7. If information is unavailable, use an empty list or null.
8. Confidence and evidence_strength must be numbers between 0 and 1.
9. Prefer specific factors over vague concepts.
10. Conditions are extremely important: preserve geography,
    population, industry, time period, technology level,
    experimental setting, or other context when available.
"""


    def _extract_json(self, text: str) -> Dict[str, Any]:
        text = text.strip()

        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?", "", text)
            text = re.sub(r"```$", "", text).strip()

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("Model did not return JSON")

        return json.loads(text[start:end + 1])

    def extract(self, paper: Dict[str, Any]) -> ExtractionResult:
        abstract = paper.get("abstract", "").strip()

        if not abstract:
            return ExtractionResult(
                paper_id=paper.get("paper_id", ""),
                source_id=paper.get("source_id", "openalex"),
                claims=[],
                factors=[],
                relationships=[],
                conditions=[],
                limitations=[],
                raw_model_output="",
            )

        prompt = self._prompt(paper)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a scientific research evidence extraction system. "
                    "Return JSON only. Never invent evidence."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=4096,
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=900,
                do_sample=False,
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

        raw_output = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        try:
            parsed = self._extract_json(raw_output)
        except ValueError:
            print("\n=== RAW MODEL OUTPUT ===")
            print(raw_output)
            print("=== END RAW MODEL OUTPUT ===\n")
            raise

        claims = parsed.get("claims", [])
        factors = parsed.get("factors", [])
        relationships = parsed.get("relationships", [])

        # Research extraction is a candidate interpretation, not ground truth.
        for claim in claims:
            claim.setdefault("provenance", {})
            claim["provenance"].update({
                "extraction_model": model_name if hasattr(self, "model_name") else MODEL_NAME,
                "status": "model_extracted_unverified",
            })

        for factor in factors:
            factor.setdefault("provenance", {})
            factor["provenance"].update({
                "extraction_model": model_name if hasattr(self, "model_name") else MODEL_NAME,
                "status": "model_extracted_unverified",
            })

        for relationship in relationships:
            relationship.setdefault("provenance", {})
            relationship["provenance"].update({
                "extraction_model": model_name if hasattr(self, "model_name") else MODEL_NAME,
                "status": "model_extracted_unverified",
            })

        return ExtractionResult(
            paper_id=paper.get("paper_id", ""),
            source_id=paper.get("source_id", "openalex"),
            claims=claims,
            factors=factors,
            relationships=relationships,
            conditions=parsed.get("conditions", []),
            limitations=parsed.get("limitations", []),
            raw_model_output=raw_output,
        )


def save_result(
    result: ExtractionResult,
    claims_dir: Path,
    factors_dir: Path,
    relationships_dir: Path,
):
    claims_dir.mkdir(parents=True, exist_ok=True)
    factors_dir.mkdir(parents=True, exist_ok=True)
    relationships_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "paper_id": result.paper_id,
        "source_id": result.source_id,
    }

    claims_path = claims_dir / f"{result.paper_id.replace('/', '_')}.json"
    factors_path = factors_dir / f"{result.paper_id.replace('/', '_')}.json"
    relationships_path = (
        relationships_dir
        / f"{result.paper_id.replace('/', '_')}.json"
    )

    claims_payload = {
        **metadata,
        "claims": result.claims,
        "conditions": result.conditions,
        "limitations": result.limitations,
    }

    factors_payload = {
        **metadata,
        "factors": result.factors,
    }

    relationships_payload = {
        **metadata,
        "relationships": result.relationships,
    }

    claims_path.write_text(
        json.dumps(claims_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    factors_path.write_text(
        json.dumps(factors_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    relationships_path.write_text(
        json.dumps(
            relationships_payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
