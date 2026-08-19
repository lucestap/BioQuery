import json

from extract import extract_evidence


with open(
    "examples/data/pfk1_ranked_papers.json",
    "r",
    encoding="utf-8",
) as file:
    ranked_papers = json.load(file)

question = (
    "How does allosteric regulation of PFK-1 work "
    "at the molecular level?"
)

selected_papers = ranked_papers[:5]

print("SELECTED PAPERS:")

for i, paper in enumerate(selected_papers, start=1):
    print(
        f"{i}. {paper['title']} "
        f"(relevance={paper['relevance_score']})"
    )

evidence = extract_evidence(
    question=question,
    papers=selected_papers,
)

print(f"\nEVIDENCE RECORDS: {len(evidence)}")

for i, record in enumerate(evidence, start=1):
    print(f"\n{i}. Paper: {record['paper_id']}")
    print(f"   Claim: {record['claim']}")
    print(f"   Aspect: {record['question_aspect']}")
    print(f"   Type: {record['evidence_type']}")
    print(f"   Support: {record['support']}")
    print(f"   Limitations: {record['limitations']}")
    print(f"   Scope: {record['source_scope']}")

with open(
    "examples/data/pfk1_evidence.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(evidence, file, indent=2)

print(
    f"\nSaved {len(evidence)} evidence records to "
    "examples/data/pfk1_evidence.json"
)