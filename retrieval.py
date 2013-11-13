from math import log
"""
	Finding relevant documents based on a search query
"""
class Retrieval:

	def __init__(self, index):
		self.index = index.index
		self.lengthOfFiles = index.lengthOfFiles
		self.N = len(index.lengthOfFiles)
		self.avgFileLength = sum(index.lengthOfFiles.values()) / float(self.N)

	def TFIDF(self, query):
		"""	The Term Frequency * Inverse Document Frequency score for a query (string list) in a document """
		# Take the documents in which all the query terms appear
		docs = set.intersection(*[set(self.index[term].keys()) for term in query])
		score = dict.fromkeys(self.lengthOfFiles.keys(), 0)
		for term in query:
			idf = log(self.N / float(len(self.index[term])))
			for doc, tf in self.index[term].items():
				if doc in docs:
					score[doc] += (1 + log(tf)) * idf
		return score

	def BM25(self, query, k = 1.5, b = 0.75): # default b and k values from http://en.wikipedia.org/wiki/Okapi_BM25#cite_ref-1
		"""	The Okapi BM25 score for a query (string list) in a document """
		# Take the documents in which all the query terms appear
		docs = set.intersection(*[set(self.index[term].keys()) for term in query])
		score = dict.fromkeys(self.lengthOfFiles.keys(), 0)
		for term in query:
			idf = log(self.N / float(len(self.index[term])))
			for doc, tf in self.index[term].items():
				if doc in docs:
					score[doc] += idf * (((k+1) * tf) / (k*((1-b) + b*(self.lengthOfFiles[doc]/self.avgFileLength)) + tf))

		return score
