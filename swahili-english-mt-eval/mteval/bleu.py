"""BLEU (Papineni et al., 2002) with optional add-one smoothing for short sentences."""
import math
from collections import Counter

from .tokenize import tokenize


def _ngrams(tokens, n):
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def _stats(hyp, refs, max_n):
    h = tokenize(hyp)
    rs = [tokenize(r) for r in refs]
    matches, totals = [], []
    for n in range(1, max_n + 1):
        hc = _ngrams(h, n)
        max_ref = Counter()
        for r in rs:
            for g, c in _ngrams(r, n).items():
                max_ref[g] = max(max_ref[g], c)
        matches.append(sum(min(c, max_ref[g]) for g, c in hc.items()))
        totals.append(max(len(h) - n + 1, 0))
    ref_len = min((abs(len(r) - len(h)), len(r)) for r in rs)[1]
    return matches, totals, len(h), ref_len


def _score(matches, totals, hyp_len, ref_len, smooth):
    precisions = []
    for m, t in zip(matches, totals):
        if smooth:
            m, t = m + 1, t + 1
        if t == 0 or m == 0:
            return 0.0
        precisions.append(m / t)
    bp = 1.0 if hyp_len > ref_len else math.exp(1 - ref_len / hyp_len) if hyp_len else 0.0
    return 100 * bp * math.exp(sum(math.log(p) for p in precisions) / len(precisions))


def sentence_bleu(hyp, refs, max_n=4, smooth=True):
    if isinstance(refs, str):
        refs = [refs]
    return _score(*_stats(hyp, refs, max_n), smooth)


def corpus_bleu(hyps, refs_list, max_n=4):
    """refs_list: one list of references per hypothesis."""
    M, T, H, R = [0] * max_n, [0] * max_n, 0, 0
    for hyp, refs in zip(hyps, refs_list):
        if isinstance(refs, str):
            refs = [refs]
        m, t, h, r = _stats(hyp, refs, max_n)
        M = [a + b for a, b in zip(M, m)]
        T = [a + b for a, b in zip(T, t)]
        H += h
        R += r
    return _score(M, T, H, R, smooth=False)
