from __future__ import annotations

import requests


EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def search_europe_pmc(query: str, page_size: int = 5) -> list[dict]:
    """Search Europe PMC and return publication records."""

    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": page_size,
    }

    response = requests.get(
        EUROPE_PMC_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("resultList", {}).get("result", [])


from clean import deduplicate_papers, simplify_paper

def search_multiple_queries(
    queries: list[str],
    page_size: int = 10,
) -> list[dict]:
    """Run multiple Europe PMC searches and combine the results."""

    all_results = []

    for query in queries:
        print(f"Searching: {query}")
        results = search_europe_pmc(
            query,
            page_size=page_size,
        )
        all_results.extend(results)

    return all_results


if __name__ == "__main__":
    queries = [
        '"PFK1" allosteric regulation',
        '"phosphofructokinase-1" structural mechanism',
        '"PFK1" regulatory sites',
    ]

    raw_results = search_multiple_queries(
        queries,
        page_size=10,
    )

    print(f"\nRaw results: {len(raw_results)}")

    unique_results = deduplicate_papers(raw_results)

    print(f"Unique results: {len(unique_results)}")

    papers = [
        simplify_paper(paper)
        for paper in unique_results
    ]

    for i, paper in enumerate(papers[:10], start=1):
        print(f"\n{i}. {paper['title']}")
        print(f"Year: {paper['year']}")
        print(f"PMID: {paper['pmid']}")
        print(f"DOI: {paper['doi']}")