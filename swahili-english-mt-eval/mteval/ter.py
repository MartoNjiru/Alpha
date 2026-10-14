"""Simplified TER: word-level edit distance (no block shifts) / reference length."""
from .tokenize import tokenize


def ter(hyp, ref):
    h, r = tokenize(hyp), tokenize(ref)
    prev = list(range(len(r) + 1))
    for i, hw in enumerate(h, 1):
        cur = [i]
        for j, rw in enumerate(r, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (hw != rw)))
        prev = cur
    return 100 * prev[-1] / max(len(r), 1)
