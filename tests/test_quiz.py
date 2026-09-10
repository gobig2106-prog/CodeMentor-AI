import unittest
from pathlib import Path

from src.history import SessionHistory
from src.knowledge_base import KnowledgeBase
from src.quiz import QuizEngine


DATASET = Path(__file__).parents[1] / "dataset" / "programming_qa.csv"


class QuizTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase(DATASET)
        cls.engine = QuizEngine(cls.kb, threshold=0.30)
        cls.record = cls.kb.records[0]

    def test_pick_question_respects_language(self):
        record = self.engine.pick_question("Java")
        self.assertEqual(record.language, "Java")

    def test_pick_question_respects_difficulty(self):
        record = self.engine.pick_question("Python", "Advanced")
        self.assertEqual(record.difficulty, "Advanced")

    def test_correct_quiz_answer(self):
        result = self.engine.evaluate(
            self.record,
            "A Python variable is a name bound to an object and assignment can bind it to a value.",
        )
        self.assertTrue(result.correct)
        self.assertGreaterEqual(result.score, 0.30)

    def test_incorrect_quiz_answer(self):
        result = self.engine.evaluate(self.record, "The database uses SQL tables and joins.")
        self.assertFalse(result.correct)

    def test_similar_quiz_answer(self):
        result = self.engine.evaluate(self.record, "A variable is a name connected to an object.")
        self.assertGreater(result.score, 0.15)

    def test_empty_quiz_answer(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate(self.record, "  ")

    def test_history_tracks_questions_and_quizzes(self):
        history = SessionHistory()
        match = self.kb.search("What is a Python list?")
        history.add_question("What is a Python list?", match)
        result = self.engine.evaluate(self.record, "A variable is a name bound to an object.")
        history.add_quiz_result(result)
        self.assertEqual(history.questions_asked, 1)
        self.assertEqual(history.questions_matched, 1)
        self.assertEqual(history.quiz_attempts, 1)
        self.assertEqual(history.quiz_correct, 1)
        self.assertGreater(history.average_similarity, 0)

    def test_clear_history(self):
        history = SessionHistory()
        history.clear()
        self.assertEqual(history.questions_asked, 0)
        self.assertEqual(history.quiz_attempts, 0)


if __name__ == "__main__":
    unittest.main()