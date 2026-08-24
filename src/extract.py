from __future__ import annotations

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv


def extract_evidence_batch(
    question: str,
    papers: list[dict],
) -> list[dict]:
    """Extract structured, question-relevant claims from paper abstracts.

    Each evidence record preserves paper provenance and explicitly records
    both supporting information and limitations. V1 is abstract-grounded;
    the function must not infer evidence from unavailable full text.
    """

    # The extractor receives only papers already selected by the relevance
    # stage; relevance itself is not treated as scientific evidence.

    papers_json = json.dumps(papers, indent=2)

    prompt = f"""
You are extracting scientific evidence relevant to a biological question.

Question:
{question}

Selected papers:
{papers_json}

Use only information explicitly supported by the supplied paper records and abstracts.
Do not use outside knowledge.
Do not fill in experimental details that are absent from an abstract.

Extract specific evidence that contributes to answering the question.
A paper may support more than one distinct evidence record.
Extract at most 3 evidence records per paper.
Prefer a small number of specific, high-value findings over exhaustive extraction.

For each evidence record:
- preserve the paper ID exactly as provided
- state one specific claim supported by the supplied abstract
- identify which aspect of the question it informs
- classify the evidence type
- briefly state what information in the abstract supports the claim
- state important limitations of what can be concluded from the supplied abstract
- record the source scope as "abstract"

Do not treat relevance as evidence.
Do not make a claim merely because a paper's title suggests it.

Return only valid JSON using exactly this structure:

{{
  "evidence": [
    {{
      "paper_id": "the paper id exactly as provided",
      "claim": "one specific claim supported by the abstract",
      "question_aspect": "the part of the biological question this informs",
      "evidence_type": "structural, biochemical, mutational, computational, review, or other",
      "support": "the abstract information supporting this claim",
      "limitations": "what cannot be concluded from the supplied abstract",
      "source_scope": "abstract"
    }}
  ]
}}

Do not include Markdown formatting or any text outside the JSON.


"""
    load_dotenv()

    client = Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=3000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Select the model's text output explicitly because a response may
    # contain other Anthropic content-block types.

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

    

    result = json.loads(response_text)

    return result["evidence"]


def extract_evidence(
    question: str,
    papers: list[dict],
    batch_size: int = 2,
) -> list[dict]:
    """Extract evidence in small batches and combine the records.

    Extraction can produce several evidence records per paper, so smaller
    batches reduce the risk of truncated model responses.
    """

    all_evidence = []

    for start in range(0, len(papers), batch_size):
        batch = papers[start:start + batch_size]

        print(
            f"Extracting evidence from papers "
            f"{start + 1}-{start + len(batch)} "
            f"of {len(papers)}"
        )

        evidence = extract_evidence_batch(
            question=question,
            papers=batch,
        )

        all_evidence.extend(evidence)

    return all_evidence