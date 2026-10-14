import argparse
import json

from .agreement import fleiss_kappa, krippendorff_alpha_nominal, pairwise_agreement, interpret
from .aggregate import majority_vote
from .gold import gold_accuracy, flag_annotators


def main(argv=None):
    p = argparse.ArgumentParser(description="Annotation quality report")
    p.add_argument("path", help="JSONL: {\"labels\": {annotator: label}, \"gold\": optional}")
    p.add_argument("--threshold", type=float, default=0.8)
    a = p.parse_args(argv)
    rows = [json.loads(l) for l in open(a.path, encoding="utf-8") if l.strip()]
    items = [r["labels"] for r in rows]
    gold = {i: r["gold"] for i, r in enumerate(rows) if r.get("gold") is not None}
    alpha = krippendorff_alpha_nominal(items)
    print(f"Items: {len(items)}  Pairwise agreement: {pairwise_agreement(items):.2f}")
    try:
        k = fleiss_kappa(items)
        print(f"Fleiss' kappa: {k:.3f} ({interpret(k)})")
    except ValueError as e:
        print(f"Fleiss' kappa: skipped ({e})")
    print(f"Krippendorff's alpha: {alpha:.3f} ({interpret(alpha)})")
    if gold:
        acc = gold_accuracy(items, gold)
        print("Gold accuracy:", {k: round(v, 2) for k, v in sorted(acc.items())})
        print("Flagged (<%.0f%%):" % (a.threshold * 100), flag_annotators(acc, a.threshold) or "none")
    print("Final labels:")
    for i, item in enumerate(items):
        lab, conf = majority_vote(item)
        print(f"  {i}: {lab} ({conf:.0%})")
