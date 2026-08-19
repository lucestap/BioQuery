from __future__ import annotations

from assess import assess_papers
from clean import deduplicate_papers, simplify_paper
from extract import extract_evidence
from planner import generate_investigation_plan
from rcsb import fetch_pdb_entry, simplify_pdb_entry
from search import search_multiple_queries
from synthesis import synthesize_investigation
from uniprot import search_uniprot, simplify_uniprot_record

def run_bioquery(
    topic: str,
    question: str,
    existing_knowledge: str,
    depth: str,
    gene: str,
    organism_id: int,
    papers_per_query: int = 5,
    evidence_papers: int = 5,
) -> dict:
    """Run the BioQuery biological investigation workflow."""

    print("1. Planning investigation...")

    plan = generate_investigation_plan(
        topic=topic,
        question=question,
        existing_knowledge=existing_knowledge,
        depth=depth,
    )

    search_queries = []

    for dimension in plan["investigation_dimensions"]:
        search_queries.extend(dimension["search_queries"])

    print(
        f"   Generated {len(search_queries)} "
        f"targeted literature searches."
    )

    print("2. Retrieving literature...")

    raw_papers = search_multiple_queries(
        search_queries,
        page_size=papers_per_query,
    )

    simplified_papers = [
        simplify_paper(paper)
        for paper in raw_papers
    ]

    unique_papers = deduplicate_papers(simplified_papers)

    print(
        f"   Retrieved {len(raw_papers)} raw records, "
        f"{len(unique_papers)} unique."
    )

    print("3. Assessing paper relevance...")

    assessments = assess_papers(
        question=question,
        papers=unique_papers,
    )

    assessments_by_id = {
        assessment["id"]: assessment
        for assessment in assessments
    }

    ranked_papers = []

    for paper in unique_papers:
        assessment = assessments_by_id.get(paper["id"])

        if assessment is None:
            continue

        ranked_papers.append(
            {
                **paper,
                "relevance_score": assessment["relevance_score"],
                "relevance_reason": assessment["reason"],
            }
        )

    ranked_papers.sort(
        key=lambda paper: paper["relevance_score"],
        reverse=True,
    )

    selected_papers = ranked_papers[:evidence_papers]

    print(
        f"   Selected top {len(selected_papers)} "
        f"papers for evidence extraction."
    )

    print("4. Extracting structured evidence...")

    literature_evidence = extract_evidence(
        question=question,
        papers=selected_papers,
    )

    print(
        f"   Extracted {len(literature_evidence)} "
        f"evidence records."
    )

    print("5. Retrieving UniProt annotation...")

    uniprot_results = search_uniprot(
        gene=gene,
        organism_id=organism_id,
    )

    if not uniprot_results:
        raise RuntimeError(
            f"No reviewed UniProt record found for "
            f"{gene} in organism {organism_id}."
        )

    protein = simplify_uniprot_record(
        uniprot_results[0]
    )

    print(
        f"   Resolved {gene} to "
        f"UniProt {protein['accession']}."
    )

    print("6. Retrieving PDB structures...")

    structures = []

    for pdb_reference in protein["pdb_structures"]:
        pdb_id = pdb_reference["pdb_id"]

        entry = fetch_pdb_entry(pdb_id)

        structures.append(
            simplify_pdb_entry(entry)
        )

    print(
        f"   Retrieved {len(structures)} "
        f"experimental structures."
    )

    print("7. Synthesizing investigation...")

    brief = synthesize_investigation(
        question=question,
        existing_knowledge=existing_knowledge,
        literature_evidence=literature_evidence,
        uniprot_record=protein,
        structures=structures,
    )

    print("   BioQuery investigation complete.")

    return {
        "input": {
            "topic": topic,
            "question": question,
            "existing_knowledge": existing_knowledge,
            "depth": depth,
            "gene": gene,
            "organism_id": organism_id,
        },
        "investigation_plan": plan,
        "retrieval": {
            "raw_paper_count": len(raw_papers),
            "unique_paper_count": len(unique_papers),
            "search_queries": search_queries,
        },
        "ranked_papers": ranked_papers,
        "selected_papers": selected_papers,
        "literature_evidence": literature_evidence,
        "uniprot": protein,
        "structures": structures,
        "research_brief": brief,
    }