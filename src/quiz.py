"""Explainable quiz selection and answer evaluation."""

from __future__ import annotations

import random
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .knowledge_base import KnowledgeBase, KnowledgeRecord
from .preprocess import preprocess_text


@dataclass(frozen=True)
class QuizResult:
    question: str
    user_answer: str
    expected_answer: str
    score: float
    correct: bool


class QuizEngine:
    def __init__(self, knowledge_base: KnowledgeBase, threshold: float = 0.35) -> None:
        if not 0 <= threshold <= 1:
            raise ValueError("Quiz threshold must be between 0 and 1.")
        self.knowledge_base = knowledge_base
        self.threshold = threshold

    def pick_question(
        self,
        language: str = "All Languages",
        difficulty: str = "All Levels",
    ) -> KnowledgeRecord:
        indexes = self.knowledge_base.filter_records(language, difficulty)
        if not indexes:
            raise ValueError("No quiz questions match the current filters.")
        return random.choice([self.knowledge_base.records[index] for index in indexes])

    def evaluate(self, record: KnowledgeRecord, user_answer: str) -> QuizResult:
        if not isinstance(user_answer, str) or not user_answer.strip():
            raise ValueError("Please write an answer before submitting.")
        vectorizer = TfidfVectorizer(
            lowercase=False,
            token_pattern=r"(?u)\b[\w+#.]+\b",
            ngram_range=(1, 2),
        )
        vectors = vectorizer.fit_transform([
            preprocess_text(record.answer),
            preprocess_text(user_answer),
        ])
        score = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])
        return QuizResult(
            question=record.question,
            user_answer=user_answer,
            expected_answer=record.answer,
            score=score,
            correct=score >= self.threshold,
        )