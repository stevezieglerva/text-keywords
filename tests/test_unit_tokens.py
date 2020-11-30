import unittest
import sys
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


if __name__ == "__main__":
    unittest.main()