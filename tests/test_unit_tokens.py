import unittest
import sys
import os
from Tokens import *
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class TokensUnitTests(unittest.TestCase):
    def test_constructor__given_two_words__then_three_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens("hello world")
        print(results)

        # Assert
        expected = """
text length:        11
token count:        3
word count:         2

top token counts:   [(1, 'hello'), (1, 'world'), (1, 'hello world')]

top bigram counts:  [(1, 'hello world')]

top trigram counts: []
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_two_words_and_email__then_three_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens("hello world test@example.com")
        print(results)

        # Assert
        expected = """
text length:        28
token count:        3
word count:         2

top token counts:   [(1, 'hello'), (1, 'world'), (1, 'hello world')]

top bigram counts:  [(1, 'hello world')]

top trigram counts: []
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_period_ending_sentence__then_correct_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens("The car drove up the hill.")
        print(results)

        # Assert
        expected = """
text length:        26
token count:        4
word count:         6

top token counts:   [(1, 'car'), (1, 'drove'), (1, 'hill'), (1, 'car drove')]

top bigram counts:  [(1, 'car drove')]

top trigram counts: []
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_two_sentences__then_correct_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens("The car drove up the hill. Then, it rolled down the hill.")
        print(results)

        # Assert
        expected = """
text length:        57
token count:        5
word count:         12

top token counts:   [(2, 'hill'), (1, 'car'), (1, 'drove'), (1, 'rolled'), (1, 'car drove')]

top bigram counts:  [(1, 'car drove')]

top trigram counts: []
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_url_included__then_correct_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens("The website is https://www.example.com.")
        print(results)

        # Assert
        expected = """
text length:        39
token count:        1
word count:         3

top token counts:   [(1, 'website')]

top bigram counts:  []

top trigram counts: []
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_trigram__then_correct_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens("The Los Angelos Kings won the cup!")
        print(results)

        # Assert
        expected = """
text length:        34
token count:        7
word count:         7

top token counts:   [(1, 'los'), (1, 'angelos'), (1, 'kings'), (1, 'cup'), (1, 'los angelos'), (1, 'angelos kings'), (1, 'los angelos kings')]

top bigram counts:  [(1, 'los angelos'), (1, 'angelos kings')]

top trigram counts: [(1, 'los angelos kings')]
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_street_address__then_correct_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens(
            "The President lives at 1600 Pennsylvania Avenue NW, Washington, DC 20500. It is the most important residence in Washington DC."
        )
        print(results)

        # Assert
        expected = """
text length:        126
token count:        18
word count:         18

top token counts:   [(2, 'washington'), (2, 'dc'), (2, 'washington dc'), (1, 'president'), (1, 'lives'), (1, 'pennsylvania'), (1, 'avenue'), (1, 'nw'), (1, 'important'), (1, 'residence'), (1, 'president lives'), (1, 'pennsylvania avenue'), (1, 'avenue nw'), (1, 'nw washington'), (1, 'pennsylvania avenue nw'), (1, 'avenue nw washington'), (1, 'nw washington dc'), (1, 'important residence')]

top bigram counts:  [(2, 'washington dc'), (1, 'president lives'), (1, 'pennsylvania avenue'), (1, 'nw washington'), (1, 'important residence'), (1, 'avenue nw')]

top trigram counts: [(1, 'pennsylvania avenue nw'), (1, 'nw washington dc'), (1, 'avenue nw washington')]
"""
        self.assertEqual(str(results), expected)

    def test_constructor__given_word_with_number__then_correct_tokens_found(
        self,
    ):
        # Arrange

        # Act
        results = Tokens("The President had COVID-19.")
        print(results)

        # Assert
        expected = """
text length:        27
token count:        2
word count:         4

top token counts:   [(1, 'president'), (1, 'covid-19')]

top bigram counts:  []

top trigram counts: []
"""
        self.assertEqual(str(results), expected)


if __name__ == "__main__":
    unittest.main()