"""Learning-mode orchestration for CodeMentor AI."""

from __future__ import annotations

from dataclasses import dataclass

from .knowledge_base import KnowledgeBase, Match


@dataclass(frozen=True)
class LearningResponse:
    question: str
    match: Match
    message: str


class CodeMentorAssistant:
    """Turns a retrieved record into an explainable study response."""

    UNKNOWN_MESSAGE = (
        "I couldn't find a relevant programming concept in the current knowledge "
        "base. Try asking about Python, Java, C, SQL, HTML/CSS, or JavaScript."
    )

    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        self.knowledge_base = knowledge_base

    def ask(
        self,
        question: str,
        language: str = "All Languages",
        difficulty: str = "All Levels",
    ) -> LearningResponse:
        match = self.knowledge_base.search(question, language, difficulty)
        if not match.matched or match.record is None:
            return LearningResponse(question, match, self.UNKNOWN_MESSAGE)
        record = match.record
        message = (
            f"Topic: {record.category}\n"
            f"Language: {record.language}\n"
            f"Difficulty: {record.difficulty}\n"
            f"Similarity score: {match.score:.2f}\n\n"
            f"Answer:\n{record.answer}\n\n"
            f"Related concepts: {', '.join(record.related_list)}"
        )
        return LearningResponse(question, match, message)