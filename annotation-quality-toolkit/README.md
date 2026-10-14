# Annotation Quality Toolkit

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen)

Quality control for data-labelling teams: measure how far annotators agree, score them on gold (known-answer) questions, and merge labels into a final answer with a confidence score.

## Features
| Module | What it does |
|---|---|
| `agreement.py` | Pairwise agreement, Fleiss' kappa (fixed raters) and Krippendorff's alpha (handles missing labels) |
| `gold.py` | Per-annotator accuracy on gold questions and flags for anyone below a threshold |
| `aggregate.py` | Majority vote, optionally weighted by annotator trust, with confidence |

## Quick start
```bash
python -m annoq examples/sentiment.jsonl
```
```
Items: 6  Pairwise agreement: 0.50
Fleiss' kappa: 0.243 (fair)
Krippendorff's alpha: 0.285 (fair)
Gold accuracy: {'ann1': 1.0, 'ann2': 1.0, 'ann3': 0.5}
Flagged (<80%): ['ann3']
Final labels:
  0: positive (100%)
  1: negative (67%)
  2: neutral (100%)
  3: negative (67%)
  4: negative (33%)
  5: positive (67%)
```

## Data format
One JSON object per line: `labels` (`{annotator: label}`) and optional `gold` (the correct label). The example mixes English and Swahili sentiment items.

## Run the tests
```bash
python -m unittest discover -s tests -v
```

## Notes
- Fleiss' kappa is checked against the classic 10-item, 14-rater table (kappa = 0.210).
- Readings follow Landis & Koch: 0.41 to 0.60 moderate, 0.61 to 0.80 substantial.
- Low agreement usually means the guidelines are unclear, not that annotators are careless. Check the confusing items first.

## License
MIT, by Martin Njiru.
