from math import sqrt, isnan
import numpy as np
"""
	Documents and queries are represented as a vector of term frequencies.
"""
class WordVector:

	def __init__(self, index, docs):
		if "cf" in docs:
			del docs["cf"]

		self.words = index.index.keys()
		self.docs = docs.keys()
	
		# Buld document vectors
		self.index = []
		for w, ind in index.index.items():
			vector = []
			for d in docs.keys():
				try:
					vector.append(ind[d])
				except KeyError:
					vector.append(0)
			self.index.append(vector)
		self.wordmatrix = np.array(self.index)

	def cosine(self, query):
		""" The cosine distance between each document vector and the query vector"""
		
		# Build the query vector
		u = np.zeros(len(self.words))
		for w in range(len(self.words)):
			u[w] = query.count(self.words[w])
		
		# Calculate cosine distance to each document vector
		score = {}
		docmatrix = self.wordmatrix.transpose()
		for d in range(len(self.docs)):
			v = docmatrix[d]
			denominator = (sqrt(np.dot(u, u)) * sqrt(np.dot(v, v)))
			if denominator != 0:
				cosine = np.dot(u, v) / denominator
			else:
				cosine = 0
			score[self.docs[d]] = cosine


		return score
