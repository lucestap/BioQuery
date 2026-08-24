import json
import sys
from pathlib import Path


sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "src"),
)

from pipeline import run_bioquery


result = run_bioquery(
    topic="AMPK energy sensing and metabolic regulation",
    question=(
        "How does AMPK sense cellular energy stress and "
        "regulate downstream metabolism at the molecular level?"
    ),
    existing_knowledge=(
        "I understand basic enzyme regulation, phosphorylation, "
        "cell signalling, and cellular metabolism."
    ),
    depth="advanced undergraduate",
    gene="PRKAA1",
    organism_id=9606,

    checkpoint_path=(
        "examples/data/ampk_pre_synthesis.json"
    ),
)

output_path = Path(
    "examples/data/ampk_complete_investigation.json"
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