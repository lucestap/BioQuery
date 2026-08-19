import json
from planner import generate_investigation_plan
from search import search_multiple_queries
from clean import deduplicate_papers, simplify_paper


plan = generate_investigation_plan(
    topic="PFK-1 allosteric regulation",
    question="How does allosteric regulation of PFK-1 work at the molecular level?",
    existing_knowledge=(
        "I understand basic enzyme kinetics, cooperativity, glycolysis, "
        "and allosteric regulation."
    ),
    depth="advanced undergraduate",
)

print(json.dumps(plan, indent=2))

search_queries = []

for dimension in plan["investigation_dimensions"]:
    search_queries.extend(dimension["search_queries"])

print("\nSEARCH QUERIES:")
for query in search_queries:
    print(f"- {query}")

papers = search_multiple_queries(
    search_queries,
    page_size=5,
)

print(f"\nRAW PAPERS RETRIEVED: {len(papers)}")

simplified_papers = [
    simplify_paper(paper)
    for paper in papers
]

unique_papers = deduplicate_papers(simplified_papers)

print(f"UNIQUE PAPERS: {len(unique_papers)}")


print("\nTOP RETRIEVED PAPERS:")

for i, paper in enumerate(unique_papers[:15], start=1):
    print(f"\n{i}. {paper['title']}")
    print(f"   Year: {paper['year']}")
    print(f"   PMID: {paper['pmid']}")
    print(f"   DOI: {paper['doi']}")