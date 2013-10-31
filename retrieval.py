from __future__ import division
from math import log
"""
	Finding relevant documents based on a search query
"""
class Retrieval:

	def __init__(self, index, corpus_size):
		self.index = index
		self.corpus_size = corpus_size

	def TFIDF(self, query):
		"""	The Term Frequency * Inverse Document Frequency score for a query (string list) in a document """
		# Take the documents in which all the query terms appear
		docs = set.intersection(*[set(self.index[term].keys()) for term in query])
		score = dict.fromkeys(docs, 0)
		for term in query:
			idf = log(self.corpus_size / len(self.index[term]))
			for doc, tf in self.index[term].items():
				if doc in docs:
					score[doc] += (1 + log(tf)) * idf
		return score