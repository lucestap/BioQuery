import json

from evaluate import precision_at_k

from clean import deduplicate_papers, simplify_paper
from search import search_multiple_queries

from evaluate import mean_precision_at_k, precision_at_k

with open(
    "examples/data/pfk1_ranked_papers.json",
    "r",
    encoding="utf-8",
) as file:
    ranked_papers = json.load(file)

print("TOP 10 BIOQUERY-RANKED PAPERS:")

for i, paper in enumerate(ranked_papers[:10], start=1):
    print(f"\n{i}. {paper['title']}")
    print(f"   PMID: {paper['pmid']}")
    print(f"   BioQuery score: {paper['relevance_score']}")


manual_labels = [1,1,1,0,1,1,1,0,0,1]

p_at_5 = precision_at_k(
    manual_labels,
    5,
)

p_at_10 = precision_at_k(
    manual_labels,
    10,
)

print(f"\nPrecision@5: {p_at_5:.2f}")
print(f"Precision@10: {p_at_10:.2f}")


baseline_queries = [
    '"PFK1" allosteric regulation',
    '"phosphofructokinase-1" structural mechanism',
    '"PFK1" regulatory sites',
]

baseline_raw = search_multiple_queries(
    baseline_queries,
    page_size=10,
)

baseline_simplified = [
    simplify_paper(paper)
    for paper in baseline_raw
]

baseline_papers = deduplicate_papers(
    baseline_simplified
)

print("\nTOP 10 BASELINE PAPERS:")

for i, paper in enumerate(
    baseline_papers[:10],
    start=1,
):
    print(f"\n{i}. {paper['title']}")
    print(f"   PMID: {paper['pmid']}")

baseline_labels = [
    1, 0, 1, 0, 1,
    0, 0, 0, 0, 0,
]

baseline_p_at_5 = precision_at_k(
    baseline_labels,
    5,
)

baseline_p_at_10 = precision_at_k(
    baseline_labels,
    10,
)

print(
    f"\nBaseline Precision@5: "
    f"{baseline_p_at_5:.2f}"
)

print(
    f"Baseline Precision@10: "
    f"{baseline_p_at_10:.2f}"
)


evaluation_cases = {
    "pfk1": {
        "question": (
            "How does allosteric regulation of PFK-1 "
            "work at the molecular level?"
        ),
        "baseline_queries": [
            '"PFK1" allosteric regulation',
            '"phosphofructokinase-1" structural mechanism',
            '"PFK1" regulatory sites',
        ],
    },
    "p53": {
        "question": (
            "How do disease-associated mutations in p53 "
            "disrupt its function at the molecular level?"
        ),
        "baseline_queries": [
            '"p53" disease mutations molecular mechanism',
            '"TP53" mutations structure function',
            '"p53" cancer mutations DNA binding stability',
        ],
    },
    "ampk": {
        "question": (
            "How does AMPK sense cellular energy stress and "
            "regulate downstream metabolism at the molecular level?"
        ),
        "baseline_queries": [
            '"AMPK" energy sensing molecular mechanism',
            '"AMPK" AMP ATP allosteric regulation',
            '"AMPK" metabolic regulation phosphorylation',
        ],
    },
}

print("\n" + "=" * 60)
print("Q2: P53 BASELINE")
print("=" * 60)

p53_raw = search_multiple_queries(
    evaluation_cases["p53"]["baseline_queries"],
    page_size=10,
)

p53_papers = deduplicate_papers(
    [
        simplify_paper(paper)
        for paper in p53_raw
    ]
)

for i, paper in enumerate(p53_papers[:10], start=1):
    print(f"\n{i}. {paper['title']}")
    print(f"   PMID: {paper['pmid']}")
    print(f"   DOI: {paper['doi']}")


print("\n" + "=" * 60)
print("Q3: AMPK BASELINE")
print("=" * 60)

ampk_raw = search_multiple_queries(
    evaluation_cases["ampk"]["baseline_queries"],
    page_size=10,
)

ampk_papers = deduplicate_papers(
    [
        simplify_paper(paper)
        for paper in ampk_raw
    ]
)

for i, paper in enumerate(ampk_papers[:10], start=1):
    print(f"\n{i}. {paper['title']}")
    print(f"   PMID: {paper['pmid']}")
    print(f"   DOI: {paper['doi']}")


p53_baseline_labels = [
    1, 0, 0, 1, 0,
    0, 1, 1, 0, 0,
]

ampk_baseline_labels = [
    0, 0, 0, 0, 1,
    0, 0, 0, 0, 0,
]

p53_baseline_duplicates = [0] * 10
ampk_baseline_duplicates = [0] * 10

print(
    "\nP53 Baseline "
    f"P@5={precision_at_k(p53_baseline_labels, 5):.2f}, "
    f"P@10={precision_at_k(p53_baseline_labels, 10):.2f}"
)

print(
    "AMPK Baseline "
    f"P@5={precision_at_k(ampk_baseline_labels, 5):.2f}, "
    f"P@10={precision_at_k(ampk_baseline_labels, 10):.2f}"
)


p53_bioquery_labels = [
    1, 1, 1, 1, 1,
    1, 0, 1, 1, 0,
]

ampk_bioquery_labels = [
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 0,
]

baseline_label_sets = [
    baseline_labels,
    p53_baseline_labels,
    ampk_baseline_labels,
]

bioquery_label_sets = [
    manual_labels,
    p53_bioquery_labels,
    ampk_bioquery_labels,
]

print("\n" + "=" * 60)
print("AGGREGATE EVALUATION")
print("=" * 60)

print(
    "Baseline mean Precision@5: "
    f"{mean_precision_at_k(baseline_label_sets, 5):.2f}"
)

print(
    "BioQuery mean Precision@5: "
    f"{mean_precision_at_k(bioquery_label_sets, 5):.2f}"
)

print(
    "Baseline mean Precision@10: "
    f"{mean_precision_at_k(baseline_label_sets, 10):.2f}"
)

print(
    "BioQuery mean Precision@10: "
    f"{mean_precision_at_k(bioquery_label_sets, 10):.2f}"
)


evaluation_results = {
    "cases": {
        "pfk1": {
            "baseline_precision_at_5": precision_at_k(
                baseline_labels,
                5,
            ),
            "baseline_precision_at_10": precision_at_k(
                baseline_labels,
                10,
            ),
            "bioquery_precision_at_5": precision_at_k(
                manual_labels,
                5,
            ),
            "bioquery_precision_at_10": precision_at_k(
                manual_labels,
                10,
            ),
        },
        "p53": {
            "baseline_precision_at_5": precision_at_k(
                p53_baseline_labels,
                5,
            ),
            "baseline_precision_at_10": precision_at_k(
                p53_baseline_labels,
                10,
            ),
            "bioquery_precision_at_5": precision_at_k(
                p53_bioquery_labels,
                5,
            ),
            "bioquery_precision_at_10": precision_at_k(
                p53_bioquery_labels,
                10,
            ),
        },
        "ampk": {
            "baseline_precision_at_5": precision_at_k(
                ampk_baseline_labels,
                5,
            ),
            "baseline_precision_at_10": precision_at_k(
                ampk_baseline_labels,
                10,
            ),
            "bioquery_precision_at_5": precision_at_k(
                ampk_bioquery_labels,
                5,
            ),
            "bioquery_precision_at_10": precision_at_k(
                ampk_bioquery_labels,
                10,
            ),
        },
    },
    "aggregate": {
        "baseline_mean_precision_at_5": mean_precision_at_k(
            baseline_label_sets,
            5,
        ),
        "baseline_mean_precision_at_10": mean_precision_at_k(
            baseline_label_sets,
            10,
        ),
        "bioquery_mean_precision_at_5": mean_precision_at_k(
            bioquery_label_sets,
            5,
        ),
        "bioquery_mean_precision_at_10": mean_precision_at_k(
            bioquery_label_sets,
            10,
        ),
    },
}


with open(
    "examples/data/evaluation_results.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        evaluation_results,
        file,
        indent=2,
    )

print(
    "\nSaved evaluation results to "
    "examples/data/evaluation_results.json"
)