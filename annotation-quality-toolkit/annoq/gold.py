from collections import defaultdict


def gold_accuracy(items, gold):
    """Accuracy of each annotator on items that have a gold label.

    items: list of {annotator: label}; gold: dict item_index -> label.
    """
    right, seen = defaultdict(int), defaultdict(int)
    for idx, label in gold.items():
        for ann, lab in items[idx].items():
            seen[ann] += 1
            right[ann] += lab == label
    return {a: right[a] / seen[a] for a in seen}


def flag_annotators(accuracy, threshold=0.8, min_items=1, seen=None):
    """Annotators whose gold accuracy falls below `threshold`."""
    return sorted(a for a, acc in accuracy.items()
                  if acc < threshold and (seen is None or seen.get(a, 0) >= min_items))
