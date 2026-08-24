from __future__ import annotations

import requests


EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def search_europe_pmc(query: str, page_size: int = 5) -> list[dict]:
    """Retrieve publication records from Europe PMC for one query."""

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

    # Fail explicitly on API errors rather than passing incomplete retrieval
    # results into later evidence-processing stages.

    response.raise_for_status()

    data = response.json()

    return data.get("resultList", {}).get("result", [])




def search_multiple_queries(
    queries: list[str],
    page_size: int = 10,
) -> list[dict]:
    """Run multiple Europe PMC searches and combine the raw results.

    Deduplication is intentionally handled downstream so the retrieval layer
    remains responsible only for communicating with Europe PMC.
    """

    all_results = []

    for query in queries:
        print(f"Searching: {query}")
        results = search_europe_pmc(
            query,
            page_size=page_size,
        )
        all_results.extend(results)

    return all_results


