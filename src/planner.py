from __future__ import annotations

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

def generate_investigation_plan(
    topic: str,
    question: str,
    existing_knowledge: str,
    depth: str,
) -> dict:
    """Generate a structured investigation plan for a biological question."""
    prompt = f"""
You are planning a focused biological investigation.

Topic: {topic}

Question: {question}

Existing knowledge:
{existing_knowledge}

Desired depth:
{depth}

Your task is to decide what evidence is needed to answer the question well.
Do not answer the biological question itself.

Break the investigation into 3 to 5 distinct evidence dimensions.
For each dimension:
- give it a concise name
- explain why it matters for answering the question
- generate 1 to 3 targeted literature search queries

Return only valid JSON using exactly this structure:

{{
  "question_interpretation": "A concise interpretation of what the question is asking",
  "investigation_dimensions": [
    {{
      "dimension": "Name of evidence dimension",
      "why_it_matters": "Why this evidence is needed",
      "search_queries": [
        "targeted search query",
        "targeted search query"
      ]
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

    

    return json.loads(response_text)