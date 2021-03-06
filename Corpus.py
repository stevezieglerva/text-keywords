from Tokens import *
import os
import re

from TopX import *


class Corpus:
    """Create a corpus object.
    Keyword arguments:
    corpus_location --- directory containing the "corpus.txt" file
    corpus_text --- string containing the text of a small corpus

    Print the returned object to get information about read corpus."""

    def __init__(self, **kwargs):
        self.location = kwargs.get("corpus_location", "")
        self.corpus_file = ""
        self.text = kwargs.get("corpus_text", "")
        self.token_meta_data = ""
        self.token_frequencies = self.__get_corpus_data()
        self.most_frequent_tokens = self.__get_frequent_tokens(10)

    def __repr__(self):
        text = """
location: {}
text: {}
token_frequencies: {}
        """
        return text.format(self.location, self.text, self.token_frequencies)

    def __str__(self):
        text = """
location:     {}
corpus_file:  {}
text:         {}
token count:  {}
"""
        corpus_text = self.text
        if len(self.text) > 100:
            corpus_text = self.text[0:100]
        return text.format(
            self.location, self.corpus_file, corpus_text, len(self.token_frequencies)
        )

    def __get_corpus_data(self):
        corpus_frequencies = {}
        if self.text == "":
            corpus_cache = os.path.join(self.location, "corpus_cache.txt")
            if os.path.isfile(corpus_cache):
                self.corpus_file = corpus_cache
                corpus_frequencies = self.__read_corpus_frequency_file(corpus_cache)
            else:
                self.corpus_file = self.location + "corpus.txt"
                tokens = self.__read_corpus_tokens_from_file(self.corpus_file)
                corpus_frequencies = tokens.token_frequencies
                self.token_meta_data = str(tokens)
                self.__create_corpus_frequency_file(
                    corpus_cache, corpus_frequencies, self.token_meta_data
                )
        else:
            tokens = Tokens(self.text)
            self.token_meta_data = str(tokens)
            corpus_frequencies = tokens.token_frequencies
        return corpus_frequencies

    def __read_corpus_tokens_from_file(self, corpus_filename):
        file_text = ""
        try:
            with open(corpus_filename, "r", encoding="utf-8") as file:
                file_text = file.read()
        except IOError as e:
            raise IOError("Can't find " + corpus_filename)
        tokens = Tokens(file_text)
        return tokens

    def __create_corpus_frequency_file(self, filename, corpus_frequencies, meta_data):
        with open(filename, "w") as file:
            meta_data_with_comments = re.sub(r"\n", "\n#", meta_data)
            meta_data_with_comments = "#" + meta_data_with_comments + "\n"
            file.write(meta_data_with_comments)
            for token in corpus_frequencies:
                line = token + "\t" + str(corpus_frequencies[token]) + "\n"
                file.write(line)
        return len(corpus_frequencies)

    def __read_corpus_frequency_file(self, corpus_frequency_filename):
        corpus_frequency = {}
        with open(corpus_frequency_filename) as file:
            line = file.readline()
            while line:
                if line.startswith("#"):
                    self.token_meta_data = self.token_meta_data + line
                else:
                    data = line.split("\t")
                    token = data[0]
                    frequency = data[1]
                    corpus_frequency[token] = float(frequency)
                line = file.readline()
        return corpus_frequency

    def create_stop_word_file(self):
        """Write the most frequent tokens to "stop_words.txt" that can be used with the Keywords class to ignore some high frequency words and return a tuple of most frequent token added to stop words and the count of stop words added."""
        total_tokens = len(self.token_frequencies)
        top_percentage = int(total_tokens * 0.01)
        print("top percentage: {}".format(top_percentage))
        top_values = TopX(top_percentage)
        count = 0
        for token in self.token_frequencies:
            count = count + 1
            if count % 1000 == 0:
                print(count)
            value = self.token_frequencies[token]
            top_values.add((value, token))

        with open("stop_words.txt", "w") as f:
            for x in top_values.values:
                print(x)
                f.write(x[1] + "\n")
        first_value = top_values.values[0]
        return (first_value, top_percentage)

    def __get_frequent_tokens(self, top_n=10):
        top_values = TopX(top_n)
        for token in self.token_frequencies:
            value = self.token_frequencies[token]
            top_values.add((value, token))
        return top_values
