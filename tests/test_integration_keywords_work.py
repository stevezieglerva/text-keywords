import unittest
import sys
import os
from Corpus import Corpus
from Keywords import Keywords
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class WorkKeywordUnitTests(unittest.TestCase):
    def test_constructor__given_gsa_fss_19__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/work/")
        keywords = Keywords(corpus)
        input = ""
        with open("./tests/data/work/combined_file_gsa.txt", "r") as file:
            input = file.read()

        # Act
        results = keywords.get_keywords(input)
        print(str(results))

        # Assert
        expected = ["gsa", "supply chain", "agile", "fss-19 systems modernization"]
        for keyword in expected:
            self.assertTrue(
                keyword in results.keywords,
                f"Expected to find '{keyword}' in {results.keywords}",
            )

    def test_constructor__given_pto__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/work/")
        keywords = Keywords(corpus)
        input = ""
        with open("./tests/data/work/combined_file_pto.txt", "r") as file:
            input = file.read()

        # Act
        results = keywords.get_keywords(input)
        print(str(results))

        # Assert
        expected = ["agile", "uspto", "devsecops"]
        for keyword in expected:
            self.assertTrue(
                keyword in results.keywords,
                f"Expected to find '{keyword}' in {results.keywords}",
            )

    def test_constructor__given_cwig__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/work/")
        keywords = Keywords(corpus)
        input = ""
        with open("./tests/data/work/combined_file_cwig.txt", "r") as file:
            input = file.read()

        # Act
        results = keywords.get_keywords(input)
        print(str(results))

        # Assert
        expected = ["cb", "child welfare", "nextgen gateway"]
        for keyword in expected:
            self.assertTrue(
                keyword in results.keywords,
                f"Expected to find '{keyword}' in {results.keywords}",
            )

    def test_constructor__given_ncea__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/work/")
        keywords = Keywords(corpus)
        input = ""
        with open("./tests/data/work/combined_file_ncea.txt", "r") as file:
            input = file.read()

        # Act
        results = keywords.get_keywords(input)
        print(str(results))

        # Assert
        expected = ["epa", "human health risk", "multiple ongoing projects"]
        for keyword in expected:
            self.assertTrue(
                keyword in results.keywords,
                f"Expected to find '{keyword}' in {results.keywords}",
            )

    def test_constructor__given_covid_news__then_correct_keywords_returned(
        self,
    ):
        # Arrange
        corpus = Corpus(corpus_location="./tests/data/work/")
        keywords = Keywords(corpus)
        input = ""
        with open("./tests/data/work/combined_file_covid_news.txt", "r") as file:
            input = file.read()

        # Act
        results = keywords.get_keywords(input)
        print(str(results))

        # Assert
        expected = ["americans", "nation"]
        for keyword in expected:
            self.assertTrue(
                keyword in results.keywords,
                f"Expected to find '{keyword}' in {results.keywords}",
            )


if __name__ == "__main__":
    unittest.main()