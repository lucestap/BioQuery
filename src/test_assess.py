import json

from assess import assess_papers


with open(
    "examples/data/pfk1_candidate_papers.json",
    "r",
    encoding="utf-8",
) as file:
    papers = json.load(file)

question = (
    "How does allosteric regulation of PFK-1 work "
    "at the molecular level?"
)

sample_papers = papers

assessments = assess_papers(
    question=question,
    papers=sample_papers,
)

assessments_by_id = {
    assessment["id"]: assessment
    for assessment in assessments
}

ranked_papers = []

for paper in papers:
    assessment = assessments_by_id.get(paper["id"])

    if assessment is None:
        continue

    ranked_paper = {
        **paper,
        "relevance_score": assessment["relevance_score"],
        "relevance_reason": assessment["reason"],
    }

    ranked_papers.append(ranked_paper)

ranked_papers.sort(
    key=lambda paper: paper["relevance_score"],
    reverse=True,
)

print(f"ASSESSED PAPERS: {len(ranked_papers)}")

print("\nTOP RANKED PAPERS:")

for i, paper in enumerate(ranked_papers[:10], start=1):
    print(f"\n{i}. {paper['title']}")
    print(f"   Score: {paper['relevance_score']}")
    print(f"   Reason: {paper['relevance_reason']}")
    print(f"   PMID: {paper['pmid']}")
    print(f"   DOI: {paper['doi']}")

with open(
    "examples/data/pfk1_ranked_papers.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(ranked_papers, file, indent=2)

print(
    f"\nSaved {len(ranked_papers)} ranked papers to "
    "examples/data/pfk1_ranked_papers.json"
)