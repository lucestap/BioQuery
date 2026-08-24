from __future__ import annotations

import requests

RCSB_ENTRY_URL = "https://data.rcsb.org/rest/v1/core/entry"


def fetch_pdb_entry(pdb_id: str) -> dict:
    """Retrieve experimental structure metadata for one RCSB PDB entry."""

    url = f"{RCSB_ENTRY_URL}/{pdb_id}"

    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

# V1 keeps structure identity and experimental metadata rather than
# downloading coordinate files or performing structural calculations.

def simplify_pdb_entry(entry: dict) -> dict:
    """Convert an RCSB response into a compact BioQuery structure record."""

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

