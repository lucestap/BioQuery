from __future__ import annotations

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

def synthesize_investigation(
    question: str,
    existing_knowledge: str,
    literature_evidence: list[dict],
    uniprot_record: dict,
    structures: list[dict],
) -> dict:
    """Synthesize evidence from literature and biological databases."""

    evidence_json = json.dumps(literature_evidence, indent=2)
    uniprot_json = json.dumps(uniprot_record, indent=2)
    structures_json = json.dumps(structures, indent=2)
    prompt = f"""
You are synthesizing a biological investigation from structured evidence.

Question:
{question}

Existing knowledge:
{existing_knowledge}

LITERATURE EVIDENCE:
{evidence_json}

UNIPROT RECORD:
{uniprot_json}

RCSB PDB STRUCTURES:
{structures_json}

Answer the biological question using only the supplied evidence.

Integrate evidence across sources rather than summarizing each source separately.

Distinguish clearly between:
- findings directly supported by the supplied literature evidence
- curated UniProt annotations
- experimentally determined structural metadata from RCSB PDB

Do not introduce biological claims from outside the supplied evidence.

The literature evidence was extracted from abstracts rather than full papers.
Do not imply that full-text methods, figures, results, or supplementary data were examined.

Where evidence is incomplete, indirect, organism-specific, or based on a review rather than direct primary evidence, make that limitation explicit.

Do not treat database annotation or the existence of a PDB structure as proof of a mechanistic claim unless the supplied evidence supports that interpretation.
    
Return only valid JSON using exactly this structure:

{{
  "question": "the biological question being investigated",
  "answer": "an evidence-grounded mechanistic synthesis answering the question",
  "key_findings": [
    {{
      "finding": "a major finding",
      "source_ids": ["PMID, UniProt accession, or PDB ID supporting it"],
      "confidence": "high, medium, or low"
    }}
  ],
  "consensus": [
    "points supported consistently across the supplied evidence"
  ],
  "uncertainties_and_disagreements": [
    "important uncertainties, limitations, or conflicting evidence"
  ],
  "evidence_gaps": [
    "important aspects of the question not adequately answered by the supplied evidence"
  ],
  "recommended_papers": [
    {{
      "paper_id": "paper identifier",
      "reason": "why this paper is particularly useful"
    }}
  ],
  "next_investigation": "the most useful next biological question or investigation based on the remaining evidence gap",
  "source_warning": "a concise warning describing the evidence limitations of this investigation"
}}

Do not include Markdown formatting or text outside the JSON.
    """
    load_dotenv()

    client = Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    text_blocks = [
        block.text
        for block in message.content
        if block.type == "text"
    ]

    if not text_blocks:
        raise RuntimeError(
            f"Claude returned no text response. "
            f"Stop reason: {message.stop_reason}"
        )

    response_text = text_blocks[0].strip()

    if response_text.startswith("```json"):
        response_text = response_text.removeprefix("```json")
        response_text = response_text.removesuffix("```")
        response_text = response_text.strip()

    return json.loads(response_text) 
   
