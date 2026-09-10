"""In-memory session history and statistics."""

from __future__ import annotations

from dataclasses import dataclass

from .knowledge_base import Match
from .quiz import QuizResult


@dataclass(frozen=True)
class HistoryEntry:
    question: str
    language: str
    topic: str
    similarity: float


class SessionHistory:
    def __init__(self) -> None:
        self.entries: list[HistoryEntry] = []
        self.quiz_attempts = 0
        self.quiz_correct = 0

    def add_question(self, question: str, match: Match) -> None:
        if match.matched and match.record is not None:
            self.entries.append(HistoryEntry(
                question=question,
                language=match.record.language,
                topic=match.record.category,
                similarity=match.score,
            ))

    def add_quiz_result(self, result: QuizResult) -> None:
        self.quiz_attempts += 1
        if result.correct:
            self.quiz_correct += 1

    def clear(self) -> None:
        self.entries.clear()
        self.quiz_attempts = 0
        self.quiz_correct = 0

    @property
    def questions_asked(self) -> int:
        return len(self.entries)

    @property
    def questions_matched(self) -> int:
        return len(self.entries)

    @property
    def average_similarity(self) -> float:
        if not self.entries:
            return 0.0
        return sum(entry.similarity for entry in self.entries) / len(self.entries)