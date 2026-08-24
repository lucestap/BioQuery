import json
import sys
from pathlib import Path


sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "src"),
)

from pipeline import run_bioquery


result = run_bioquery(
    topic="Disease-associated p53 mutations",
    question=(
        "How do disease-associated mutations in p53 "
        "disrupt its function at the molecular level?"
    ),
    existing_knowledge=(
        "I understand basic protein structure, DNA binding, "
        "transcriptional regulation, and cancer biology."
    ),
    depth="advanced undergraduate",
    gene="TP53",
    organism_id=9606,
)

output_path = Path(
    "examples/data/p53_complete_investigation.json"
)

with output_path.open(
    "w",
    encoding="utf-8",
) as file:
    json.dump(result, file, indent=2)

print(
    "\nSaved complete investigation to "
    f"{output_path}"
)

print("\nTOP 10 BIOQUERY-RANKED PAPERS:")

for i, paper in enumerate(
    result["ranked_papers"][:10],
    start=1,
):
    print(f"\n{i}. {paper['title']}")
    print(f"   PMID: {paper['pmid']}")
    print(f"   DOI: {paper['doi']}")
    print(
        f"   BioQuery score: "
        f"{paper['relevance_score']}"
    )