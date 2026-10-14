import argparse
import json

from .bleu import sentence_bleu, corpus_bleu
from .chrf import chrf
from .ter import ter


def main(argv=None):
    p = argparse.ArgumentParser(description="Score translations with BLEU, chrF and TER")
    p.add_argument("path", help="JSONL with source, hypothesis, reference")
    p.add_argument("--worst", type=int, default=3, help="show the N lowest chrF sentences")
    a = p.parse_args(argv)
    rows = [json.loads(l) for l in open(a.path, encoding="utf-8") if l.strip()]
    hyps = [r["hypothesis"] for r in rows]
    refs = [[r["reference"]] for r in rows]
    scored = [(chrf(r["hypothesis"], r["reference"]), r) for r in rows]
    print(f"Sentences: {len(rows)}")
    print(f"Corpus BLEU: {corpus_bleu(hyps, refs):.1f}")
    print(f"Mean chrF:   {sum(s for s, _ in scored) / len(scored):.1f}")
    print(f"Mean TER:    {sum(ter(r['hypothesis'], r['reference']) for r in rows) / len(rows):.1f}  (lower is better)")
    print(f"\nLowest {a.worst} by chrF:")
    for s, r in sorted(scored, key=lambda x: x[0])[:a.worst]:
        print(f"  chrF {s:5.1f} | BLEU {sentence_bleu(r['hypothesis'], r['reference']):5.1f}")
        print(f"    src: {r['source']}\n    hyp: {r['hypothesis']}\n    ref: {r['reference']}")
