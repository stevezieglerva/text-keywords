from Corpus import Corpus
from Keywords import Keywords
from Tokens import *
import json


class SetTag:
    def __init__(self, set_tag_name, options):
        self.set_tag_name = set_tag_name
        self.options = options

    def __str__(self):
        text = f"""set_tag_name: {self.set_tag_name}
options: {self.options}"""
        return text

    def __repr__(self):
        return self.__str__()


class ClassiferResults:
    def __init__(self, keywords, set_tags):
        self.keywords = keywords
        self.set_tags = set_tags


class TextClassifer:
    def __init__(self, corpus_path, text="", **kwargs):
        self.__set_tags_list = kwargs.get("set_tags", [])
        self.corpus_path = corpus_path
        self.text = text
        self.corpus = Corpus(corpus_location=corpus_path)
        self.__keywords_obj = Keywords(self.corpus)
        self.set_tags = {}

    def classify_text(self, text):
        keywords = self.__keywords_obj.get_keywords(text)
        set_tags = self.__determine_set_tags(text)
        results = ClassiferResults(keywords.keywords, set_tags)
        return results

    def __determine_set_tags(self, text):
        self.__tokens = Tokens(text)
        print(self.__tokens)

        set_tags = {}

        for set_tag in self.__set_tags_list:
            top = TopX(2)
            print(set_tag)
            option_found = False
            for option in set_tag.options:
                count = self.__tokens.token_counts[option]
                print(f"{option}={count}")
                top.add((count, option))
                if count >= 2:
                    option_found = True
            if option_found:
                most_frequent_term_info = top.values[0]
                second_most_frequent_term_info = top.values[1]
                if most_frequent_term_info[0] > second_most_frequent_term_info[0]:
                    set_tags[set_tag.set_tag_name] = most_frequent_term_info[1]
                else:
                    set_tags[set_tag.set_tag_name] = ""
            else:
                set_tags[set_tag.set_tag_name] = ""
        print(json.dumps(set_tags, indent=3))
        return set_tags