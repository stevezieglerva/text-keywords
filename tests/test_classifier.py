import unittest
from Classifier import TextClassifer, SetTag
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class ClassifierUnitTests(unittest.TestCase):
    def setUp(self):
        corpus_location = "./tests/data/hockey/"

        fruit_set_tag = SetTag("fruit", ["apples", "bananas", "pears"])
        years_set_tag = SetTag("year", ["2020", "2019", "2018"])

        self.classifer = TextClassifer(
            corpus_location, set_tags=[fruit_set_tag, years_set_tag]
        )

    def test_constructor__given_simple_document__then_keywords_are_correct(self):
        # Arrange
        text_to_classify = "Ovi score the goal in the playoff game."

        # Act
        results = self.classifer.classify_text(text_to_classify)

        # Assert
        self.assertEqual(results.keywords, ["score", "goal"])

    def test_constructor__given_simple_document_fruit__then_tags_are_correct(self):
        # Arrange
        corpus_location = "./tests/data/hockey/"
        text_to_classify = "Apples are the most popular fruit, beating out bananas and pears. Apples grow across the US. "

        # Act
        results = self.classifer.classify_text(text_to_classify)

        # Assert
        self.assertEqual(results.set_tags["fruit"], "apples")

    def test_constructor__given_not_enough_apple_references__then_tag_not_determined(
        self,
    ):
        # Arrange
        corpus_location = "./tests/data/hockey/"
        text_to_classify = (
            "Apples are the most popular fruit, beating out bananas and pears."
        )
        set_tags = SetTag("fruit", ["apples", "bananas", "pears"])

        # Act
        results = self.classifer.classify_text(text_to_classify)

        # Assert
        self.assertEqual(results.set_tags["fruit"], "")

    def test_constructor__given_tags_tie_in_count__then_tag_not_determined(
        self,
    ):
        # Arrange
        corpus_location = "./tests/data/hockey/"
        text_to_classify = "Apples are the most popular fruit, beating out bananas and pears. But, I would eat apples over bananas any day"
        set_tags = SetTag("fruit", ["apples", "bananas", "pears"])

        # Act
        results = self.classifer.classify_text(text_to_classify)

        # Assert
        self.assertEqual(results.set_tags["fruit"], "")

    def test_constructor__given_simple_document_years__then_tags_are_correct(self):
        # Arrange
        corpus_location = "./tests/data/hockey/"
        text_to_classify = "Ovi won the cup in 2018. He had a good year in 2019, but 2018 was the best."
        set_tags = SetTag("year", ["2020", "2019", "2018"])

        # Act
        results = self.classifer.classify_text(text_to_classify)

        # Assert
        self.assertEqual(results.set_tags["year"], "2018")


if __name__ == "__main__":
    unittest.main()