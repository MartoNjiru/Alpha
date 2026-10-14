# Annotation & Translation QA

![tests](https://github.com/MartoNjiru/annotation-translation-qa/actions/workflows/tests.yml/badge.svg) ![python](https://img.shields.io/badge/python-3.10%2B-blue) ![deps](https://img.shields.io/badge/dependencies-none-brightgreen) ![license](https://img.shields.io/badge/license-MIT-green)

Quality-assurance tools for **human-labelled data and translation**, with a focus on English and Swahili.

| Project | What it answers | Key techniques |
|---|---|---|
| [annotation-quality-toolkit](annotation-quality-toolkit) | Do our annotators agree, and who needs retraining? | Fleiss' kappa, Krippendorff's alpha, gold-question accuracy, weighted majority vote |
| [swahili-english-mt-eval](swahili-english-mt-eval) | How good is this translation, and which sentences need a human? | Corpus BLEU, chrF, TER, worst-sentence report |

## Try it
```bash
git clone https://github.com/MartoNjiru/annotation-translation-qa.git
cd annotation-translation-qa/swahili-english-mt-eval
python -m mteval examples/sw_en.jsonl
```

## Why Swahili
Swahili is agglutinative: one word such as *wanacheza* ("they are playing") carries subject, tense and verb. Word-level metrics like BLEU undercount good Swahili translations, so this repo pairs BLEU with character-level chrF and shows the weakest sentences for a native speaker to review.

## Author
**Martin Njiru**, AI trainer and English/Swahili language specialist based in Kenya. Open to annotation, translation-QA and AI-training work: martinnjiru35@gmail.com

Related: [LLM Evaluation Toolkit](https://github.com/MartoNjiru/llm-evaluation-toolkit).

MIT licensed.
