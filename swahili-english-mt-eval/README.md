# Swahili-English MT Eval

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen)

Machine-translation evaluation built from scratch and tuned for Swahili-English work: corpus BLEU, chrF and TER, plus a report of the weakest sentences for human review.

## Features
| Module | What it does |
|---|---|
| `bleu.py` | Sentence and corpus BLEU with brevity penalty, multiple references and add-one smoothing |
| `chrf.py` | Character n-gram F-score, more forgiving for agglutinative Swahili (*wanacheza* = they-are-playing) |
| `ter.py` | Translation edit rate (word-level edit distance, no shifts) |

## Quick start
```bash
python -m mteval examples/sw_en.jsonl --worst 2
```
```
Sentences: 6
Corpus BLEU: 52.1
Mean chrF:   69.4
Mean TER:    32.9  (lower is better)

Lowest 2 by chrF:
  chrF  21.1 | BLEU  16.8
    src: Watoto wanacheza mpira uwanjani.
    hyp: The kids play ball in the field.
    ref: The children are playing football on the pitch.
  chrF  43.7 | BLEU  34.6
    src: Mvua imenyesha sana jana usiku.
    hyp: Rain fell a lot last night.
    ref: It rained heavily last night.
```

## Data format
One JSON object per line: `source`, `hypothesis` (machine output), `reference` (human translation).

## Run the tests
```bash
python -m unittest discover -s tests -v
```

## Notes
- BLEU punishes valid paraphrases: "The kids play ball" vs "The children are playing football". Read the lowest-scoring sentences yourself before blaming the model.
- Use corpus BLEU for reporting; sentence BLEU is noisy and only for triage.

## License
MIT, by Martin Njiru.
