import json

from uniprot import search_uniprot, simplify_uniprot_record


results = search_uniprot(
    gene="PFKL",
    organism_id=9606,
)

if not results:
    raise RuntimeError("No reviewed UniProt record found.")

protein = simplify_uniprot_record(results[0])

print(json.dumps(protein, indent=2))

with open(
    "examples/data/pfk1_uniprot.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(protein, file, indent=2)

print("\nSaved UniProt record to examples/data/pfk1_uniprot.json")