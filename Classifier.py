from Corpus import Corpus
from Keywords import Keywords


class SetTag:
    def __init__(self, set_tag_name, options):
        self.set_tag_name = set_tag_name
        self.options = options


class TextClassifer:
    def __init__(self, corpus_path, text, **kwargs):
        self.__set_tags_list = kwargs.get("set_tags", [])
        self.corpus_path = corpus_path
        self.text = text
        self.corpus = Corpus(corpus_location=corpus_path)
        self.__keywords_obj = Keywords(self.corpus)
        self.keywords = self.__keywords_obj.get_keywords(self.text).keywords
        self.set_tags = {}
        self.set_tags["year"] = "2018"