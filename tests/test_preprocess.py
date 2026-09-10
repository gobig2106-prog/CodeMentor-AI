import unittest

from src.preprocess import (
    normalize_text,
    preprocess_text,
    remove_stopwords,
    tokenize,
)


class PreprocessTests(unittest.TestCase):
    def test_lowercase_and_extra_spaces(self):
        self.assertEqual(normalize_text("  Python   LIST! "), "python list")

    def test_punctuation_is_handled(self):
        self.assertEqual(normalize_text("SQL, joins?"), "sql joins")

    def test_tokenization(self):
        self.assertEqual(tokenize("HTML/CSS and C++"), ["html", "css", "and", "c++"])

    def test_stopwords_do_not_remove_technical_terms(self):
        result = remove_stopwords(["what", "is", "a", "class", "in", "java"])
        self.assertIn("class", result)
        self.assertIn("java", result)
        self.assertNotIn("what", result)

    def test_preprocess_returns_searchable_text(self):
        result = preprocess_text("Explain Python lists!")
        self.assertIn("python", result)
        self.assertIn("list", result)

    def test_non_string_is_rejected(self):
        with self.assertRaises(TypeError):
            normalize_text(4)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()