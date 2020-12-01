from Corpus import Corpus
from Keywords import Keywords
from Tokens import *


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


class TextClassifer:
    def __init__(self, corpus_path, text, **kwargs):
        self.__set_tags_list = kwargs.get("set_tags", [])
        self.corpus_path = corpus_path
        self.text = text
        self.corpus = Corpus(corpus_location=corpus_path)
        self.__keywords_obj = Keywords(self.corpus)
        self.keywords = self.__keywords_obj.get_keywords(self.text).keywords
        self.set_tags = {}

        self.__tokens = Tokens(text)
        print(self.__tokens)

        top = TopX(2)
        for set_tag in self.__set_tags_list:
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
                    self.set_tags[set_tag.set_tag_name] = most_frequent_term_info[1]
                else:
                    self.set_tags[set_tag.set_tag_name] = ""
            else:
                self.set_tags[set_tag.set_tag_name] = ""