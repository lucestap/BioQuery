from __future__ import annotations

import requests


UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"


def search_uniprot(
    gene: str,
    organism_id: int = 9606,
) -> list[dict]:
    """Retrieve reviewed UniProt entries matching a gene and organism.

    ``organism_id`` accepts an NCBI taxonomy identifier; 9606 (human) is
    provided only as a convenient default rather than a pipeline restriction.
    """

    params = {
        "query": (
            f"gene_exact:{gene} "
            f"AND organism_id:{organism_id} "
            f"AND reviewed:true"
        ),
        "format": "json",
        "size": 5,
    }

    response = requests.get(
        UNIPROT_SEARCH_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])


def simplify_uniprot_record(record: dict) -> dict:
    """Extract protein identity, function, functional sites, and PDB links.

    The compact representation retains curated biological annotations and
    their evidence metadata while discarding fields not used by BioQuery V1.
    """

    protein_description = record.get("proteinDescription", {})
    recommended_name = protein_description.get("recommendedName", {})
    protein_name = recommended_name.get("fullName", {}).get("value")

    genes = record.get("genes", [])
    gene = None

    if genes:
        gene = genes[0].get("geneName", {}).get("value")

    organism = record.get("organism", {})

    function_texts = []



    for comment in record.get("comments", []):
        if comment.get("commentType") == "FUNCTION":
            for text in comment.get("texts", []):
                function_texts.append(text.get("value"))

    catalytic_activities = []

    for comment in record.get("comments", []):
        if comment.get("commentType") == "CATALYTIC ACTIVITY":
            reaction = comment.get("reaction", {})

            catalytic_activities.append(
                {
                    "reaction": reaction.get("name"),
                    "ec_number": reaction.get("ecNumber"),
                }
            )

    functional_sites = []

    # Retain only site annotations that can contribute directly to molecular
    # interpretation of catalytic or ligand-binding mechanisms.

    for feature in record.get("features", []):
        if feature.get("type") not in {"Binding site", "Active site"}:
            continue

        location = feature.get("location", {})

        functional_sites.append(
            {
                "type": feature.get("type"),
                "start": location.get("start", {}).get("value"),
                "end": location.get("end", {}).get("value"),
                "description": feature.get("description"),
                "ligand": feature.get("ligand"),
                "evidence": feature.get("evidences", []),
            }
        )

    pdb_structures = []

    # UniProt provides the curated bridge from protein identity to relevant
    # experimental structures used by the RCSB retrieval stage.

    for reference in record.get("uniProtKBCrossReferences", []):
        if reference.get("database") != "PDB":
            continue

        properties = {
            item.get("key"): item.get("value")
            for item in reference.get("properties", [])
        }

        pdb_structures.append(
            {
                "pdb_id": reference.get("id"),
                "method": properties.get("Method"),
                "resolution": properties.get("Resolution"),
                "chains": properties.get("Chains"),
            }
        )

    return {
        "source": "UniProt",
        "accession": record.get("primaryAccession"),
        "entry": record.get("uniProtkbId"),
        "gene": gene,
        "protein_name": protein_name,
        "organism": organism.get("scientificName"),
        "organism_id": organism.get("taxonId"),
        "function": function_texts,
        "catalytic_activity": catalytic_activities,
        "functional_sites": functional_sites,
        "pdb_structures": pdb_structures,
    }