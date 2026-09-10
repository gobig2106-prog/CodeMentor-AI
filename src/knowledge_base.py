"""Dataset loading, validation, filtering, and TF-IDF retrieval."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .preprocess import preprocess_text

REQUIRED_COLUMNS = {
    "id", "question", "answer", "language", "category", "difficulty",
    "keywords", "related_topics",
}
SUPPORTED_LANGUAGES = ("All Languages", "Python", "Java", "C", "SQL", "HTML/CSS", "JavaScript")
SUPPORTED_DIFFICULTIES = ("All Levels", "Beginner", "Intermediate", "Advanced")


@dataclass(frozen=True)
class KnowledgeRecord:
    id: int
    question: str
    answer: str
    language: str
    category: str
    difficulty: str
    keywords: str
    related_topics: str

    @property
    def related_list(self) -> list[str]:
        return [item.strip() for item in self.related_topics.split(";") if item.strip()]


@dataclass(frozen=True)
class Match:
    record: KnowledgeRecord | None
    score: float
    matched: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "record": asdict(self.record) if self.record else None,
            "score": self.score,
            "matched": self.matched,
        }


class KnowledgeBaseError(RuntimeError):
    """Raised when the local knowledge base cannot be used safely."""


class KnowledgeBase:
    """A small, transparent TF-IDF index over programming questions."""

    def __init__(self, csv_path: str | Path, threshold: float = 0.30) -> None:
        if not 0 <= threshold <= 1:
            raise ValueError("Similarity threshold must be between 0 and 1.")
        self.csv_path = Path(csv_path)
        self.threshold = threshold
        self.records = self._load_records()
        if not self.records:
            raise KnowledgeBaseError("The knowledge base is empty.")
        self._vectorizer = TfidfVectorizer(
            lowercase=False,
            token_pattern=r"(?u)\b[\w+#.]+\b",
            ngram_range=(1, 2),
        )
        self._matrix = self._vectorizer.fit_transform(
            preprocess_text(record.question) for record in self.records
        )

    def _load_records(self) -> list[KnowledgeRecord]:
        if not self.csv_path.exists():
            raise KnowledgeBaseError(f"Dataset not found: {self.csv_path}")
        try:
            frame = pd.read_csv(self.csv_path, dtype=str).fillna("")
            missing = REQUIRED_COLUMNS - set(frame.columns)
            if missing:
                raise KnowledgeBaseError(
                    f"Dataset is missing required columns: {', '.join(sorted(missing))}"
                )
            records = []
            for row_number, row in enumerate(frame.to_dict(orient="records"), start=2):
                try:
                    records.append(KnowledgeRecord(
                        id=int(row["id"]),
                        question=row["question"].strip(),
                        answer=row["answer"].strip(),
                        language=row["language"].strip(),
                        category=row["category"].strip(),
                        difficulty=row["difficulty"].strip(),
                        keywords=row["keywords"].strip(),
                        related_topics=row["related_topics"].strip(),
                    ))
                except (KeyError, TypeError, ValueError) as exc:
                    raise KnowledgeBaseError(
                        f"Invalid dataset record at CSV row {row_number}: {exc}"
                    ) from exc
            return records
        except (OSError, pd.errors.ParserError, UnicodeError) as exc:
            raise KnowledgeBaseError(f"Could not read dataset: {exc}") from exc

    def filter_records(
        self,
        language: str = "All Languages",
        difficulty: str = "All Levels",
    ) -> list[int]:
        """Return record indexes matching the selected filters."""
        return [
            index for index, record in enumerate(self.records)
            if (language in ("All", "All Languages") or record.language == language)
            and (difficulty in ("All", "All Levels") or record.difficulty == difficulty)
        ]

    def search(
        self,
        question: str,
        language: str = "All Languages",
        difficulty: str = "All Levels",
    ) -> Match:
        """Return the best filtered match, or an explicit unmatched result."""
        if not isinstance(question, str) or not question.strip():
            raise ValueError("Please enter a programming question.")
        candidate_indexes = self.filter_records(language, difficulty)
        if not candidate_indexes:
            return Match(None, 0.0, False)
        processed_question = preprocess_text(question)
        query_terms = set(processed_question.split())
        vector = self._vectorizer.transform([processed_question])
        scores = cosine_similarity(vector, self._matrix[candidate_indexes]).ravel()
        best_position = int(np.argmax(scores))
        score = float(scores[best_position])
        record = self.records[candidate_indexes[best_position]]
        # A generic word such as "explain" should never make an unrelated
        # record look relevant. Require at least one meaningful term from the
        # selected record's question/keywords before accepting the score.
        concept_terms = set(preprocess_text(record.keywords).split())
        has_concept_overlap = bool(query_terms & concept_terms)
        return Match(record, score, score >= self.threshold and has_concept_overlap)

    def to_json(self, path: str | Path) -> None:
        """Export the validated records for inspection or demos."""
        Path(path).write_text(
            json.dumps([asdict(record) for record in self.records], indent=2),
            encoding="utf-8",
        )