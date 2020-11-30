import unittest
import sys
import os
from Corpus import Corpus
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class CorpusUnitTests(unittest.TestCase):
    def test_constructor__given_literal_corpus_text__then_corpus_loaded(
        self,
    ):
        # Arrange

        # Act
        results = Corpus(corpus_text="hello world")
        print(results)

        # Assert
        expected = """
location:     
corpus_file:  
text:         hello world
token count:  3
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_literal_corpus_text_with_stop_words__then_stop_words_not_counted(
        self,
    ):
        # Arrange

        # Act
        results = Corpus(corpus_text="hello world. this does not count.")
        print(results)

        # Assert
        expected = """
location:     
corpus_file:  
text:         hello world. this does not count.
token count:  4
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_hockey_corpus__then_corpus_created(
        self,
    ):
        # Arrange
        if os.path.exists("./tests/data/hockey/corpus_cache.txt"):
            os.remove("./tests/data/hockey/corpus_cache.txt")

        # Act
        results = Corpus(corpus_location="./tests/data/hockey/")
        print(results)

        # Assert
        expected = """
location:     ./tests/data/hockey/
corpus_file:  ./tests/data/hockey/corpus.txt
text:         
token count:  3747
"""
        self.assertEqual(str(results), expected)

    def test_create_stop_word_file__given_hockey_corpus__then_correct_first_value_is_returned(
        self,
    ):
        # Arrange
        if os.path.exists("./tests/data/hockey/corpus_cache.txt"):
            os.remove("./tests/data/hockey/corpus_cache.txt")
        corpus = Corpus(corpus_location="./tests/data/hockey/")

        # Act
        results = ""
        with patch("builtins.open", unittest.mock.mock_open()) as m:
            results = corpus.create_stop_word_file()

        # Assert
        self.assertEqual(results, ((0.013704558568955569, "nhl"), 37))


if __name__ == "__main__":
    unittest.main()