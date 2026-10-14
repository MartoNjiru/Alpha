from collections import Counter


def majority_vote(item, weights=None):
    """Return (label, confidence). `weights` maps annotator -> trust (default 1).

    Ties are broken alphabetically so results are reproducible.
    """
    weights = weights or {}
    score = Counter()
    for ann, label in item.items():
        score[label] += weights.get(ann, 1.0)
    total = sum(score.values())
    label = sorted(score.items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0]
    return label, (score[label] / total if total else 0.0)
