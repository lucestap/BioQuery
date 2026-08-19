import json

from synthesis import synthesize_investigation

with open(
    "examples/data/pfk1_evidence.json",
    "r",
    encoding="utf-8",
) as file:
    literature_evidence = json.load(file)

with open(
    "examples/data/pfk1_uniprot.json",
    "r",
    encoding="utf-8",
) as file:
    uniprot_record = json.load(file)

with open(
    "examples/data/pfk1_structures.json",
    "r",
    encoding="utf-8",
) as file:
    structures = json.load(file)

question = (
    "How does allosteric regulation of PFK-1 work "
    "at the molecular level?"
)

existing_knowledge = (
    "I understand basic enzyme kinetics, cooperativity, glycolysis, "
    "and allosteric regulation."
)

brief = synthesize_investigation(
    question=question,
    existing_knowledge=existing_knowledge,
    literature_evidence=literature_evidence,
    uniprot_record=uniprot_record,
    structures=structures,
)

print(json.dumps(brief, indent=2))

with open(
    "examples/data/pfk1_research_brief.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(brief, file, indent=2)

print(
    "\nSaved research brief to "
    "examples/data/pfk1_research_brief.json"
)