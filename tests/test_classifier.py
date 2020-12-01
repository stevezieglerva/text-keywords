import unittest
from Classifier import TextClassifer, SetTag
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class ClassifierUnitTests(unittest.TestCase):
    def test_constructor__given_simple_document__then_keywords_are_correct(self):
        # Arrange
        corpus_location = "./tests/data/hockey/"
        text_to_classify = "Ovi score the goal in the playoff game."

        # Act
        results = TextClassifer(corpus_location, text_to_classify)

        # Assert
        self.assertEqual(results.keywords, ["score", "goal"])

    def test_constructor__given_simple_document__then_tags_are_correct(self):
        # Arrange
        corpus_location = "./tests/data/hockey/"
        text_to_classify = "Ovi score the goal in the 2018 playoff game. His goals in 2020 were down from 2018."
        set_tags = SetTag("year", ["2020", "2019", "2018"])

        # Act
        results = TextClassifer(corpus_location, text_to_classify, set_tags=[set_tags])

        # Assert
        self.assertEqual(results.set_tags["year"], "2018")


if __name__ == "__main__":
    unittest.main()