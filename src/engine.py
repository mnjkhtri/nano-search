from collections import defaultdict
import string

import numpy as np
import pandas as pd

class SearchEngine:
    def __init__(self, k1 = 1.2, b = 0.75):
        # A word -> {URL : Number of that word in the URL}
        self._index: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        # URL -> Content
        self._documents: dict[str, str] = {}
        # Normalization constansts
        self.k1 = k1
        self.b = b

    @staticmethod
    def normalize_string(input: str):
        # Remove the punctutation characters:
        without_punc = input.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
        # Lower case the strings:
        lower_case = without_punc.lower()
        return lower_case

    @property
    def number_of_documents(self): return len(self._documents)

    @property
    def avdl(self): return np.mean([len(d) for d in self._documents.values()])

    def index_from_df(self, contents: pd.DataFrame):
        """
        Populates the search index from a DataFrame containing URL and content pairs.
        """
        for url, content in contents.itertuples(index=False):
            self._documents[url] = content
            words = SearchEngine.normalize_string(content).split(" ")
            for word in words:
                self._index[word][url] += 1

    def get_urls_that_contain_a_keyword(self, keyword: str) -> dict[str, int]:
        return self._index[self.normalize_string(keyword)]
    
    def idf(self, kw: str):
        n_kw = len(self.get_urls_that_contain_a_keyword(kw))
        return np.log((self.number_of_documents - n_kw + 0.5)/(n_kw + 0.5)+1)

    def bm25(self, kw: str):
        result = {}
        idf = self.idf(kw)
        for url, tf in self.get_urls_that_contain_a_keyword(kw).items():
            scale_tf = tf * (self.k1 + 1)
            scale_ln = self.b * len(self._documents[url]) / self.avdl
            form = scale_tf / (tf + self.k1 * (1 - self.b + scale_ln))
            result[url] = form * idf
        return result 
    
    def search(self, query: str):
        url_scores = {}
        for kw in self.normalize_string(query).split(" "):
            kw_score =  self.bm25(kw)
            for url, score in kw_score.items():
                if url in url_scores: url_scores[url] += score
                else: url_scores[url] = score
        return url_scores
    
    def search_top_10(self, query: str):
        search_results = self.search(query)
        return sorted(search_results.items(), key=lambda x: x[1], reverse=True)[:10]

engine = SearchEngine()