# import nltk
# from nltk.corpus import stopwords
import string
from collections import Counter
from collections import OrderedDict
import datetime
import re
from TimerCollection import *
from TopX import *
import os.path


class Tokens:
    def __init__(self, text):
        self.TOPN_COUNT = 20
        self.text = text
        self.word_count = 0
        self.token_counts = self.__get_token_counts()
        self.token_frequencies = self.__get_token_frequency()
        self.token_1gram_counts = []
        for token in self.token_counts.most_common(self.TOPN_COUNT):
            # reverse the tuple from Counter to match the TopX
            self.token_1gram_counts.append((token[1], token[0]))
        print(str(self))

    def __str__(self):
        text = """
text length:        {}
token count:        {}
word count:         {}

top token counts:   {}

top bigram counts:  {}

top trigram counts: {}
"""
        top_tokens = (
            str(self.token_1gram_counts).encode("ascii", "ignore").decode("ascii")
        )
        top_bigrams = (
            str(self.token_bigram_counts).encode("ascii", "ignore").decode("ascii")
        )
        top_trigrams = (
            str(self.token_trigram_counts).encode("ascii", "ignore").decode("ascii")
        )
        str_version = text.format(
            len(self.text),
            len(self.token_counts),
            self.word_count,
            top_tokens,
            top_bigrams,
            top_trigrams,
        )
        return str_version

    def get_top_grams_list(self):
        list = []
        for token in self.token_1gram_counts:
            list.append(token[1])
        for token in self.token_bigram_counts:
            list.append(token[1])
        for token in self.token_trigram_counts:
            list.append(token[1])
        return list

    def __get_tokens(self, text):
        t = TimerCollection()
        t.start_timer("10 - Total Process")
        t.start_timer("15 - First Half")
        lowers = text.lower()
        # remove the punctuation using the character deletion step of translate
        # 		print(datetime.now())
        lowers = re.sub("[^ ]+@[^ ]+", " ", lowers)

        # 		print("Removing punc")
        no_punctuation = lowers.translate(
            str.maketrans("", "", string.punctuation.replace("-", ""))
        )

        # 		print(datetime.now())
        # 		print("Getting tokens")
        t.start_timer("13 - tokenize")
        tokens = nltk.word_tokenize(no_punctuation)
        self.word_count = len(tokens)
        t.end_timer("13 - tokenize")
        # 		print(datetime.now())
        # 		print("Filter tokens")
        stopwords_eng = stopwords.words("english")
        if os.path.exists("stop_words.txt"):
            extra_stop_words = []
            with open("stop_words.txt", "r") as f:
                extra_stop_words = f.read().splitlines()
            stopwords_eng = stopwords_eng + extra_stop_words
        filtered = [w for w in tokens if not w in stopwords_eng]

        t.start_timer("14 - counter")
        self.tokens_1 = Counter(filtered)
        t.end_timer("14 - counter")
        t.end_timer("15 - First Half")

        t.start_timer("17 - Second Half")
        avg_tokens_per_byte = 0.045
        expected_tokens = int(len(self.text) / avg_tokens_per_byte)

        bigram_filtered = [expected_tokens]
        trigram_filtered = [expected_tokens]

        # 		print(datetime.now())
        # 		print("Getting grams")
        t.start_timer("50 - sentences")
        sentences = nltk.sent_tokenize(lowers)
        t.end_timer("25 - sentences")
        sent_total = len(sentences)
        sent_count = 0
        for sentence in sentences:
            sent_count = sent_count + 1
            if sent_count % 5000 == 0:
                print(
                    str(datetime.now())
                    + " sentence {} / {}".format(sent_count, sent_total)
                )
            t.start_timer("55 - sent punctuation")
            no_punctuation = sentence.translate(
                str.maketrans("", "", string.punctuation.replace("-", ""))
            )
            t.end_timer("55 - sent punctuation")

            t.start_timer("57 - tokenize sent words")
            sentence_tokens = nltk.word_tokenize(no_punctuation)
            t.end_timer("57 - tokenize sent words")

            t.start_timer("60 - nltk.bigrams")
            bigrams = nltk.bigrams(sentence_tokens)
            t.end_timer("60 - nltk.bigrams")
            for bigram in bigrams:
                word_1 = bigram[0]
                word_2 = bigram[1]
                bigram_string = word_1 + " " + word_2
                if (
                    bigram_string not in stopwords_eng
                    and word_1 not in stopwords_eng
                    and word_2 not in stopwords_eng
                ):
                    t.start_timer("65 - appending")
                    filtered.append(bigram_string)
                    bigram_filtered.append(bigram_string)
                    t.end_timer("65 - appending")

            t.start_timer("70 - nltk.trigrams")
            trigrams = nltk.trigrams(sentence_tokens)
            t.end_timer("70 - nltk.trigrams")
            for trigram in trigrams:
                word_1 = trigram[0]
                word_2 = trigram[1]
                word_3 = trigram[2]
                trigram_string = word_1 + " " + word_2 + " " + word_3
                if (
                    trigram_string not in stopwords_eng
                    and word_1 not in stopwords_eng
                    and word_2 not in stopwords_eng
                    and word_3 not in stopwords_eng
                ):
                    t.start_timer("75 - appending")
                    filtered.append(trigram_string)
                    trigram_filtered.append(trigram_string)
                    t.end_timer("75 - appending")

        t.start_timer("85 - Counters- Heap")
        counts = {}
        for bigram in bigram_filtered:
            if bigram in counts:
                counts[bigram] = counts[bigram] + 1
            else:
                counts[bigram] = 1
        top = TopX(self.TOPN_COUNT)
        for bigram in counts:
            combo = (counts[bigram], str(bigram))
            top.add(combo)
        self.token_bigram_counts = top.values

        counts = {}
        for trigram in trigram_filtered:
            if trigram in counts:
                counts[trigram] = counts[trigram] + 1
            else:
                counts[trigram] = 1
        top = TopX(self.TOPN_COUNT)
        for trigram in counts:
            combo = (counts[trigram], str(trigram))
            top.add(combo)
        self.token_trigram_counts = top.values
        t.end_timer("85 - Counters- Heap")

        t.end_timer("17 - Second Half")
        t.end_timer("10 - Total Process")
        # t.print_results()
        return filtered

    def __get_token_counts(self):
        token_counts = Counter(self.__get_tokens(self.text))
        return token_counts

    def __get_token_frequency(self):
        total_token_count = 0
        for token in self.token_counts:
            total_token_count += self.token_counts[token]

        token_ranks = {}
        for token in self.token_counts:
            ascii_token_str = token.encode("ascii", "ignore").decode("ascii")
            token_ranks[ascii_token_str] = self.token_counts[token] / total_token_count
        return token_ranks

    def get_most_common_tokens(self, limit=10):
        return self.token_counts.most_common(limit)
