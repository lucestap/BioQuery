import json
import sys
from pathlib import Path


sys.path.insert(
    0,
    str(Path(__file__).parent / "src"),
)

from pipeline import run_bioquery


result = run_bioquery(
    topic="PFK-1 allosteric regulation",
    question=(
        "How does allosteric regulation of PFK-1 "
        "work at the molecular level?"
    ),
    existing_knowledge=(
        "I understand basic enzyme kinetics, cooperativity, glycolysis, "
        "and allosteric regulation."
    ),
    depth="advanced undergraduate",
    gene="PFKL",
    organism_id=9606,
)

output_path = Path(
    "examples/data/pfk1_complete_investigation.json"
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