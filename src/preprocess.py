"""Text preparation used by the learning and quiz engines.

The implementation deliberately keeps technical words such as ``class`` and
``array``. A generic stop-word list can remove those terms and hurt retrieval.
NLTK's lemmatizer is used when its optional resource is available; the built-in
normalization remains fully offline and is the reliable fallback.
"""

from __future__ import annotations

import re
from typing import Iterable

BASE_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "does", "for",
    "from", "how", "i", "in", "is", "it", "of", "on", "or", "the", "to",
    "what", "when", "where", "which", "why", "with", "you", "your",
}
TECHNICAL_KEEP_WORDS = {
    "python", "java", "javascript", "sql", "html", "css", "class", "object",
    "function", "list", "tuple", "dictionary", "array", "loop", "inheritance",
    "polymorphism", "exception", "database", "variable", "string", "pointer",
    "query", "table", "dom", "json", "api",
}


def normalize_text(text: str) -> str:
    """Lowercase, normalize punctuation, and collapse extra whitespace."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    lowered = text.lower()
    cleaned = re.sub(r"[^a-z0-9+#.\s]", " ", lowered)
    return re.sub(r"\s+", " ", cleaned).strip()


def tokenize(text: str) -> list[str]:
    """Return normalized word-like tokens while retaining technical symbols."""
    normalized = normalize_text(text)
    return re.findall(r"[a-z][a-z0-9+#.]*", normalized)


def remove_stopwords(tokens: Iterable[str]) -> list[str]:
    """Remove conversational filler but preserve programming vocabulary."""
    return [
        token for token in tokens
        if token not in BASE_STOPWORDS or token in TECHNICAL_KEEP_WORDS
    ]


def lemmatize_tokens(tokens: Iterable[str]) -> list[str]:
    """Lemmatize when NLTK data exists; otherwise apply safe light rules."""
    token_list = list(tokens)
    try:
        from nltk.stem import WordNetLemmatizer

        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(token) for token in token_list]
    except (ImportError, LookupError):
        result = []
        for token in token_list:
            if len(token) > 4 and token.endswith("ies"):
                token = token[:-3] + "y"
            elif len(token) > 4 and token.endswith("s") and not token.endswith("ss"):
                token = token[:-1]
            result.append(token)
        return result


def preprocess_text(text: str) -> str:
    """Run the complete offline preprocessing pipeline."""
    return " ".join(lemmatize_tokens(remove_stopwords(tokenize(text))))