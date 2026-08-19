from __future__ import annotations

from typing import Any


def simplify_paper(paper: dict[str, Any]) -> dict[str, Any]:
    """Convert a Europe PMC record into a clean BioQuery paper record."""

    journal_info = paper.get("journalInfo", {})
    journal = journal_info.get("journal", {})

    return {
        "id": paper.get("pmid") or paper.get("doi") or paper.get("id"),
        "pmid": paper.get("pmid"),
        "pmcid": paper.get("pmcid"),
        "doi": paper.get("doi"),
        "title": paper.get("title"),
        "authors": paper.get("authorString"),
        "journal": journal.get("title"),
        "year": paper.get("pubYear"),
        "abstract": paper.get("abstractText"),
        "publication_type": paper.get("pubTypeList", {}).get("pubType", []),
        "open_access": paper.get("isOpenAccess") == "Y",
        "cited_by_count": paper.get("citedByCount"),
    }

def paper_identifier(paper: dict[str, Any]) -> str | None:
    """Return the most reliable identifier available for a paper."""

    if paper.get("pmid"):
        return f"pmid:{paper['pmid']}"

    if paper.get("doi"):
        return f"doi:{paper['doi'].lower()}"

    title = paper.get("title")

    if title:
        return f"title:{title.strip().lower()}"

    return None

def deduplicate_papers(
    papers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Remove duplicate papers using stable identifiers."""

    seen: set[str] = set()
    unique: list[dict[str, Any]] = []

    for paper in papers:
        identifier = paper_identifier(paper)

        if identifier is None:
            continue

        if identifier in seen:
            continue

        seen.add(identifier)
        unique.append(paper)

    return unique