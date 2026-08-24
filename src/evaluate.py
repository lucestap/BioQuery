from __future__ import annotations


def precision_at_k(
    relevance_labels: list[int],
    k: int,
) -> float:
    """Calculate the fraction of the top-k papers labelled relevant."""

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    top_k = relevance_labels[:k]

    if not top_k:
        return 0.0

    relevant = sum(
        1
        for label in top_k
        if label == 1
    )

    return relevant / len(top_k)

def mean_precision_at_k(
    label_sets: list[list[int]],
    k: int,
) -> float:
    """Calculate mean precision@k across evaluation cases."""

    if not label_sets:
        return 0.0

    scores = [
        precision_at_k(labels, k)
        for labels in label_sets
    ]

    return sum(scores) / len(scores)