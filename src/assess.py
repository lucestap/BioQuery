from __future__ import annotations

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv


def assess_paper_batch(
    question: str,
    papers: list[dict],
) -> list[dict]:
    """Score a batch of papers for question-specific relevance.

    Judgements are restricted to the supplied paper metadata and abstracts
    so relevance assessment does not rely on the model's outside knowledge.
    """
    # Pass compact, standardized records rather than raw Europe PMC responses.

    papers_json = json.dumps(papers, indent=2)

    prompt = f"""
You are assessing scientific papers for relevance to a specific biological question.

Question:
{question}

Candidate papers:
{papers_json}

Assess each paper only using the information provided in its record.
Do not use outside knowledge to infer evidence that is not present.

For each paper, assign a relevance score:

3 = directly addresses the biological question and provides highly relevant mechanistic evidence
2 = provides useful supporting or contextual evidence for part of the question
1 = biologically related, but unlikely to contribute meaningful evidence to answering the question
0 = irrelevant to the question

If the abstract is missing or insufficient, be conservative about the score.
    
Return only valid JSON using exactly this structure:

{{
  "assessments": [
    {{
      "id": "the paper id exactly as provided",
      "relevance_score": 0,
      "reason": "A concise explanation grounded only in the provided paper record"
    }}
  ]
}}

Return one assessment for every candidate paper.
Do not omit papers.
Do not include Markdown formatting or any text outside the JSON.
    """

    load_dotenv()

    client = Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # Anthropic responses can contain non-text blocks, so explicitly select
    # the text output rather than assuming the first block contains JSON.

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

    return result["assessments"]


def assess_papers(
    question: str,
    papers: list[dict],
    batch_size: int = 8,
) -> list[dict]:
    """Assess candidate papers in batches and combine the results.

    Batching keeps prompt and output sizes predictable and avoids sending
    large retrieval sets through a single LLM request.
    """
    all_assessments = []

    for start in range(0, len(papers), batch_size):
        batch = papers[start:start + batch_size]

        print(
            f"Assessing papers "
            f"{start + 1}-{start + len(batch)} "
            f"of {len(papers)}"
        )

        assessments = assess_paper_batch(
            question=question,
            papers=batch,
        )

        all_assessments.extend(assessments)

    return all_assessments
