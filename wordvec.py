from math import sqrt
"""
	Building wordvectors, defined as the vector of document frequencies.
	Document and query vectors are then wordvector sums

	Very slow because we're not using numpy
"""
class WordVector:

	def __init__(self, index, docs):
		self.index = index.index
		self.docs = docs
		if "cf" in self.docs:
			del self.docs["cf"]

		# wordvectors is index: words * docs

		# docvectors is a square matrix: docs * docs
		self.docvectors = dict.fromkeys(self.docs.keys(), dict.fromkeys(self.docs.keys(), 0))
		for doc, tokens in self.docs.items():
			for term in tokens:
				for dim, val in self.index[term].items():
					if dim in self.docvectors[doc]:
						self.docvectors[doc][dim] += val

		print "first docvector: ", self.docvectors.itervalues().next().values()


	def cosine(self, query):
		""" The cosine distance between document frequency word vectors"""
		if "cf" in self.docs:
			del self.docs["cf"]

		queryvector = dict.fromkeys(self.docs.keys(), 0)
		for term in query:
			for dim, val in self.index[term].items():
				if dim in queryvector:
					queryvector[dim] += val
		
		print "queryvector: ", queryvector.values()

		score = dict.fromkeys(self.docs.keys(), 0)
		for doc in self.docs.keys():
			numerator = 0
			for dim in self.docs.keys():
				numerator += queryvector[dim] * self.docvectors[doc][dim]

			denominator = 0
			denominator += sqrt(sum(map(lambda x: x**2, queryvector.values()))) 
			denominator += sqrt(sum(map(lambda x: x**2, self.docvectors[doc].values())))

			score[doc] = numerator / denominator

		return score
