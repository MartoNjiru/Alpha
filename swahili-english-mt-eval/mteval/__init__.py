"""Dependency-free MT metrics: BLEU, chrF, TER."""
from .bleu import sentence_bleu, corpus_bleu
from .chrf import chrf
from .ter import ter
__all__ = ["sentence_bleu", "corpus_bleu", "chrf", "ter"]
