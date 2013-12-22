from math import sqrt, isnan
import numpy as np
"""
	Building wordvectors, defined as the vector of document frequencies.
	Document and query vectors are then wordvector sums

	Very slow because we're not using numpy
"""
class WordVector:

	def __init__(self, index, docs):
		if "cf" in docs:
			del docs["cf"]

		self.words = index.index.keys()
		self.docs = docs.keys()

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
		""" The cosine distance between document frequency word vectors"""
		
		u = np.zeros(len(self.words))
		for w in range(len(self.words)):
			u[w] = query.count(self.words[w])

		score = {}
		docmatrix = self.wordmatrix.transpose()
		for d in range(len(self.docs)):
			v = docmatrix[d]
			den = (sqrt(np.dot(u, u)) * sqrt(np.dot(v, v)))
			if den != 0:
				cosine = np.dot(u, v) / den
			else:
				cosine = 0
			score[self.docs[d]] = cosine


		return score
