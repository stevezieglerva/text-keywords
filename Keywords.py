from Tokens import *
from Corpus import *
import math
import re
from esc import *


class Keywords:
	""" Keywords class """

	def __init__(self, corpus):
		self.corpus = corpus
		self.__scores = {}
	

	def get_keywords(self, text, top_n=20):
		""" Returns an array of ranked keywords based on algorithms of short and long text """
		tokens = Tokens(text)
		if tokens.word_count < 1000:
			print("*** short text")
			return self.__get_keywords_short(tokens, top_n)
		return self.__get_keywords_frequent_tokens(tokens, top_n)


	def __get_keywords_short(self, tokens, top_n=20):
		""" Returns an array of ranked keywords based on TF/IDF using a corpus """
		token_frequency = tokens.token_frequencies
		token_ranks = {}
		for token in token_frequency:
			current_token_frequency = token_frequency[token]
			current_corpus_frequency = .0001
			if token in self.corpus.token_frequencies:
				current_corpus_frequency = self.corpus.token_frequencies[token]
			rank = math.log((current_token_frequency * 2) / current_corpus_frequency)
			formula = "{0: <30}\t{1: <30}\t= \tmath.log(({2} * 2) / {3} )".format(token, rank, current_token_frequency, current_corpus_frequency)
			self.__scores[token] = formula
			token_ranks[token] = rank
			sorted_token_ranks = sorted(token_ranks, key=token_ranks.get, reverse=True)

		max_keywords = self.__get_max_viable_keyword_count(len(tokens.text))
		if top_n > max_keywords:
			top_n = max_keywords
		top_tokens_with_compound_parts = sorted_token_ranks[:top_n]
		top_tokens_without_compound_parts = self.__remove_versions_of_compound_words_from_list(top_tokens_with_compound_parts)

		results = KeywordResults(top_tokens_without_compound_parts, str(token), tokens.get_top_grams_list())
		return results


	
	def __get_keywords_frequent_tokens(self, tokens, top_n=20):
		""" Returns an array of ranked keywords based on TF in long documents favoring trigrams and bigrams first """
		possible_keywords = []
		top_keyword_scores = TopX(50)
		max_1gram_count = tokens.token_1gram_counts[0][0]

		# Get most popular trigrams if enough
		MAX_COUNT_FOR_CONSIDERATION = 2
		max_trigram_count = tokens.token_trigram_counts[0][0]
		normalizing_multiplier = int(max_1gram_count / max_trigram_count)
		print("trigram normalizing_multiplier: " + str(normalizing_multiplier))
		for token in tokens.token_trigram_counts:
			count = token[0]
			token_text = token[1]
			if count > MAX_COUNT_FOR_CONSIDERATION:
				possible_keywords.append(token_text)
				self.__scores[token_text] = str(count)
				top_keyword_scores.add((count * normalizing_multiplier, token_text))

		# Get most popular bigrams if enough
		max_bigram_count = tokens.token_bigram_counts[0][0]
		normalizing_multiplier = int(max_1gram_count / max_bigram_count)
		print("bigram normalizing_multiplier: " + str(normalizing_multiplier))
		for token in tokens.token_bigram_counts:
			count = token[0]
			token_text = token[1]
			if count > MAX_COUNT_FOR_CONSIDERATION:
				possible_keywords.append(token_text)
				self.__scores[token_text] = str(count)
				top_keyword_scores.add((count * normalizing_multiplier, token_text))

		# Add the 1 grams
		for token in tokens.token_1gram_counts:
			count = token[0]
			token_text = token[1]
			possible_keywords.append(token_text)
			self.__scores[token_text] = str(count)
			top_keyword_scores.add((count, token_text))

		top_score_keywords = [x[1] for x in top_keyword_scores.values]
		top_score_keywords = self.__remove_versions_of_compound_words_from_list(top_score_keywords)

		# Trim the keywords
		trimmed_possible = [w.strip() for w in possible_keywords]

		# filter out empty strings
		max_keywords = self.__get_max_viable_keyword_count(len(tokens.text))
		if top_n > max_keywords:
			top_n = max_keywords

		top_keywords = self.__remove_versions_of_compound_words_from_list(top_score_keywords)
		no_empty_strings = [w for w in top_keywords if self.__token_has_text(w)]

		results = KeywordResults(no_empty_strings[:max_keywords], str(token), tokens.get_top_grams_list())
		return results



	def __token_has_text(self, token):
		if esc(token) != "":
			return True
		else:
			return False


	def __get_max_viable_keyword_count(self, text_length):
		if text_length <= 100:
			return 2
		if text_length <= 200:
			return 3
		if text_length <= 1000:
			return 5
		if text_length <= 10000:
			return 10
		return 20
			

	def __remove_versions_of_compound_words_from_list(self, input_list):
		compound_word_parts = []
		for token in input_list:
			if " " in token:
				parts = token.split(" ")
				for word in parts:
					if word not in compound_word_parts:
						compound_word_parts.append(word)

		words_used_in_list = {}
		results = []
		for token in input_list:
			token_words = token.split(" ")
			new_words_found = True
			for token_word in token_words:
				if token_word in words_used_in_list:
					new_words_found = False
					break
			if new_words_found:
				for token_word in token_words:
					if token_word not in words_used_in_list:
						words_used_in_list[token_word] = "added"
				results.append(token)

		return results


	def get_formula_for_token(self, token):
		if token in self.__scores:
			return self.__scores[token] 
		return ""

	
class KeywordResults:
	def __init__(self, keywords, token_details, top_grams):
		self.keywords = keywords
		self.token_details = token_details
		self.top_grams = top_grams


	def __str__(self):
		text = """
# Keywords: {}
# Top Grams: {}
"""
		return text.format(self.keywords, str(self.top_grams))
