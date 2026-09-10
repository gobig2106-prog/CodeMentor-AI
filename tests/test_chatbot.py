import unittest
from pathlib import Path

from src.chatbot import CodeMentorAssistant
from src.knowledge_base import KnowledgeBase, KnowledgeBaseError


DATASET = Path(__file__).parents[1] / "dataset" / "programming_qa.csv"


class ChatbotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = KnowledgeBase(DATASET, threshold=0.20)
        cls.assistant = CodeMentorAssistant(cls.kb)

    def test_dataset_has_six_languages_and_150_records(self):
        self.assertEqual(len(self.kb.records), 150)
        self.assertEqual(
            {record.language for record in self.kb.records},
            {"Python", "Java", "C", "SQL", "HTML/CSS", "JavaScript"},
        )

    def test_exact_question(self):
        response = self.assistant.ask("What is a list in Python?")
        self.assertTrue(response.match.matched)
        self.assertEqual(response.match.record.language, "Python")

    def test_paraphrased_question(self):
        response = self.assistant.ask("Explain Java inheritance")
        self.assertTrue(response.match.matched)

    def test_short_question(self):
        response = self.assistant.ask("SQL joins")
        self.assertTrue(response.match.matched)

    def test_uppercase_question(self):
        response = self.assistant.ask("WHAT IS A PYTHON DICTIONARY?")
        self.assertTrue(response.match.matched)

    def test_lowercase_question(self):
        response = self.assistant.ask("what is html")
        self.assertTrue(response.match.matched)

    def test_unknown_question(self):
        response = self.assistant.ask("Explain astrophysics and black holes")
        self.assertFalse(response.match.matched)
        self.assertIn("couldn't find", response.message)

    def test_empty_question(self):
        with self.assertRaises(ValueError):
            self.assistant.ask("")

    def test_python_question(self):
        self.assertEqual(self.assistant.ask("What is a Python generator?").match.record.language, "Python")

    def test_java_question(self):
        self.assertEqual(self.assistant.ask("What is a Java interface?").match.record.language, "Java")

    def test_c_question(self):
        self.assertEqual(self.assistant.ask("What is a pointer in C?").match.record.language, "C")

    def test_sql_question(self):
        self.assertEqual(self.assistant.ask("What is a SQL transaction?").match.record.language, "SQL")

    def test_html_question(self):
        self.assertEqual(self.assistant.ask("How do hyperlinks work in HTML?").match.record.language, "HTML/CSS")

    def test_css_question(self):
        response = self.assistant.ask("Explain CSS flexbox", language="HTML/CSS")
        self.assertEqual(response.match.record.language, "HTML/CSS")

    def test_javascript_question(self):
        self.assertEqual(self.assistant.ask("What is a JavaScript promise?").match.record.language, "JavaScript")

    def test_language_filter(self):
        response = self.assistant.ask("What is inheritance?", language="Java")
        self.assertEqual(response.match.record.language, "Java")

    def test_difficulty_filter(self):
        response = self.assistant.ask(
            "What is a generator in Python?", language="Python", difficulty="Advanced"
        )
        self.assertEqual(response.match.record.difficulty, "Advanced")

    def test_related_topics_are_parsed(self):
        response = self.assistant.ask("What is a Python list?")
        self.assertGreater(len(response.match.record.related_list), 1)

    def test_missing_dataset(self):
        with self.assertRaises(KnowledgeBaseError):
            KnowledgeBase("does-not-exist.csv")


if __name__ == "__main__":
    unittest.main()