import re


def tokenize(text):
    """Lowercase, split punctuation off words (works for Swahili and English)."""
    return re.findall(r"\w+|[^\w\s]", text.lower(), re.U)
