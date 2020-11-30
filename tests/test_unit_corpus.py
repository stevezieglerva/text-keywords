import unittest
from Corpus import Corpus
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class CorpusUnitTests(unittest.TestCase):
    def test_constructor__given_corpus_file_exists_without_cache__then_corpus_loaded(
        self,
    ):
        # Arrange

        # Act
        results = Corpus("")

        # Assert
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()