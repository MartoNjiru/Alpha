"""Inter-annotator agreement.

`items` is always a list of dicts: {annotator_id: label}. Missing labels are allowed
for Krippendorff's alpha; Fleiss' kappa needs the same number of raters per item.
"""
from collections import Counter
from itertools import combinations


def pairwise_agreement(items):
    """Share of annotator pairs (over all items) that chose the same label."""
    agree = total = 0
    for item in items:
        for a, b in combinations(item.values(), 2):
            total += 1
            agree += a == b
    return agree / total if total else 0.0


def fleiss_kappa(items):
    if not items:
        raise ValueError("no items")
    n = len(items[0])
    if n < 2 or any(len(i) != n for i in items):
        raise ValueError("Fleiss' kappa needs the same number (>=2) of raters per item")
    categories = sorted({lab for i in items for lab in i.values()})
    N = len(items)
    p_j = Counter()
    P_i = []
    for item in items:
        counts = Counter(item.values())
        p_j.update(counts)
        P_i.append((sum(c * c for c in counts.values()) - n) / (n * (n - 1)))
    P_bar = sum(P_i) / N
    P_e = sum((p_j[c] / (N * n)) ** 2 for c in categories)
    if P_e == 1:
        return 1.0
    return (P_bar - P_e) / (1 - P_e)


def krippendorff_alpha_nominal(items):
    """Krippendorff's alpha for nominal data; tolerates missing labels."""
    coincidence = Counter()
    for item in items:
        labels = list(item.values())
        m = len(labels)
        if m < 2:
            continue
        for i, a in enumerate(labels):
            for j, b in enumerate(labels):
                if i != j:
                    coincidence[(a, b)] += 1 / (m - 1)
    n_c = Counter()
    for (a, _b), v in coincidence.items():
        n_c[a] += v
    n = sum(n_c.values())
    if n <= 1:
        raise ValueError("not enough pairable labels")
    D_o = sum(v for (a, b), v in coincidence.items() if a != b) / n
    D_e = sum(n_c[a] * n_c[b] for a in n_c for b in n_c if a != b) / (n * (n - 1))
    if D_e == 0:
        return 1.0
    return 1 - D_o / D_e


def interpret(score):
    """Landis & Koch style reading of a kappa/alpha value."""
    if score < 0:
        return "poor"
    for limit, word in [(0.2, "slight"), (0.4, "fair"), (0.6, "moderate"), (0.8, "substantial")]:
        if score <= limit:
            return word
    return "almost perfect"
