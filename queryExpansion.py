from retrieval import Retrieval

class queryExpansion:

"""
	Expand query with most similar words in top 50 documents.
"""

	def __init__(self):

	def getScores(self, query, method, index):
		# get scores of all documents for a particular query and method, returns dict

		return scores

	def createExpansionIndex(self, scores):
		# create inverted index for top 50 documents

		return expansionIndex


	def expandQuery(self, expansionIndex, query):
		# retrieve best query expansion terms from expansionIndex and concatenate to original query

		return expandedQuery