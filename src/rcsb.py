from __future__ import annotations

import requests


RCSB_ENTRY_URL = "https://data.rcsb.org/rest/v1/core/entry"


def fetch_pdb_entry(pdb_id: str) -> dict:
    """Fetch metadata for a PDB structure from RCSB PDB."""

    url = f"{RCSB_ENTRY_URL}/{pdb_id}"

    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def simplify_pdb_entry(entry: dict) -> dict:
    """Convert an RCSB PDB entry into a compact BioQuery structure record."""

    experimental_methods = [
        experiment.get("method")
        for experiment in entry.get("exptl", [])
        if experiment.get("method")
    ]

    return {
        "source": "RCSB PDB",
        "pdb_id": entry.get("rcsb_id"),
        "title": entry.get("struct", {}).get("title"),
        "experimental_methods": experimental_methods,
        "resolution": entry.get(
            "rcsb_entry_info",
            {},
        ).get("resolution_combined"),
        "deposit_date": entry.get(
            "rcsb_accession_info",
            {},
        ).get("deposit_date"),
    }

