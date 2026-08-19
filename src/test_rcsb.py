import json

from rcsb import fetch_pdb_entry, simplify_pdb_entry


with open(
    "examples/data/pfk1_uniprot.json",
    "r",
    encoding="utf-8",
) as file:
    protein = json.load(file)

pdb_ids = [
    structure["pdb_id"]
    for structure in protein["pdb_structures"]
]

structures = []

for pdb_id in pdb_ids:
    print(f"Fetching PDB: {pdb_id}")

    entry = fetch_pdb_entry(pdb_id)
    structure = simplify_pdb_entry(entry)

    structures.append(structure)

print("\nSTRUCTURES:")

for structure in structures:
    print(f"\n{structure['pdb_id']}: {structure['title']}")
    print(f"Method: {structure['experimental_methods']}")
    print(f"Resolution: {structure['resolution']}")

with open(
    "examples/data/pfk1_structures.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(structures, file, indent=2)

print(
    f"\nSaved {len(structures)} structures to "
    "examples/data/pfk1_structures.json"
)