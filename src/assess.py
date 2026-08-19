from __future__ import annotations

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

def assess_papers(
    question: str,
    papers: list[dict],
) -> list[dict]:
    """Assess how directly retrieved papers address a biological question."""

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

    response_text = next(
        block.text
        for block in message.content
        if block.type == "text"
    ).strip()

    if response_text.startswith("```json"):
        response_text = response_text.removeprefix("```json")
        response_text = response_text.removesuffix("```")
        response_text = response_text.strip()

    result = json.loads(response_text)

    return result["assessments"]
