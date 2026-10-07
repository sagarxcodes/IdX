import json
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

root = Path.cwd()

files = sorted(
    (root / "data/research/papers/normalized").glob("openalex_*.jsonl")
)

if not files:
    raise FileNotFoundError("No normalized OpenAlex corpus found.")

with files[-1].open(encoding="utf-8") as f:
    paper = json.loads(next(line for line in f if line.strip()))

title = paper.get("title", "")
abstract = paper.get("abstract", "")

print("=== IdX QWEN EXTRACTION TEST ===")
print("Model:", MODEL_NAME)
print("Paper:", title)

device = "mps" if torch.backends.mps.is_available() else "cpu"
print("Device:", device)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if device == "mps" else torch.float32,
)

model.to(device)
model.eval()

schema = {
    "claims": [
        {
            "text": "",
            "claim_type": "finding",
            "factors": [],
            "direction": "unknown",
            "effect_size": None,
            "effect_unit": "",
            "confidence": 0.0,
            "evidence_strength": 0.0,
            "conditions": [],
            "limitations": [],
        }
    ],
    "factors": [
        {
            "name": "",
            "category": "",
            "description": "",
            "measurable_variables": [],
        }
    ],
    "relationships": [
        {
            "source_factor": "",
            "target_factor": "",
            "relation": "",
            "direction": "unknown",
            "conditions": [],
        }
    ],
    "conditions": [],
    "limitations": [],
}

prompt = f"""You are the research extraction engine of IdX, an evidence-driven
decision intelligence system.

Analyze the research paper below.

Extract only information explicitly supported by the paper abstract.
Do not invent facts.
Do not turn correlation into causation.
Preserve uncertainty, population, geography, industry, time period and study
conditions when available.

Identify:
1. research claims/findings
2. meaningful decision factors
3. relationships between factors
4. conditions under which findings apply
5. limitations

A factor is a meaningful variable, mechanism, constraint, resource, behavior,
market driver, operational driver, economic variable, technological variable,
risk, outcome or other decision-relevant construct.

Do NOT extract cosmetic details.

Return ONLY valid JSON matching this structure:

{json.dumps(schema, indent=2)}

PAPER TITLE:
{title}

PAPER ABSTRACT:
{abstract}
"""

inputs = tokenizer(
    prompt,
    return_tensors="pt",
    truncation=True,
    max_length=4096,
)

inputs = {k: v.to(device) for k, v in inputs.items()}

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=1200,
        do_sample=False,
        temperature=None,
        top_p=None,
    )

generated = output[0][inputs["input_ids"].shape[1]:]

raw = tokenizer.decode(
    generated,
    skip_special_tokens=True,
)

print("\n=== RAW MODEL OUTPUT ===")
print(raw)
print("=== END OUTPUT ===")

try:
    parsed = json.loads(raw)
    print("\n=== JSON VALIDATION ===")
    print("VALID JSON")
    print("Claims:", len(parsed.get("claims", [])))
    print("Factors:", len(parsed.get("factors", [])))
    print("Relationships:", len(parsed.get("relationships", [])))
    print("Conditions:", len(parsed.get("conditions", [])))
    print("Limitations:", len(parsed.get("limitations", [])))
except Exception as exc:
    print("\n=== JSON VALIDATION ===")
    print("INVALID JSON:", exc)
