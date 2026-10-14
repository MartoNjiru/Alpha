"""chrF (Popovic, 2015): character n-gram F-score. Robust for agglutinative
languages like Swahili, where one word carries subject, tense and object."""
from collections import Counter


def _char_ngrams(text, n):
    s = "".join(text.lower().split())
    return Counter(s[i:i + n] for i in range(len(s) - n + 1))


def chrf(hyp, ref, max_n=6, beta=2.0):
    precs, recs = [], []
    for n in range(1, max_n + 1):
        h, r = _char_ngrams(hyp, n), _char_ngrams(ref, n)
        if not h or not r:
            continue
        overlap = sum((h & r).values())
        precs.append(overlap / sum(h.values()))
        recs.append(overlap / sum(r.values()))
    if not precs:
        return 0.0
    p, r = sum(precs) / len(precs), sum(recs) / len(recs)
    if p + r == 0:
        return 0.0
    b2 = beta ** 2
    return 100 * (1 + b2) * p * r / (b2 * p + r)
