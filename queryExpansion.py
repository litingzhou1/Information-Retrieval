from retrieval import Retrieval
from preProcess import PreProcess
import operator

class QueryExpansion:

	"""
	Expand query with most similar words in top 50 documents.
	"""

	def __init__(self,index,documents,query,method):
		self.documents = documents.listOfFiles
		self.index = index					#token-->filename-->freq
		self.method = method
		self.query = query


	def getTopDocs(self):
		"""
		# get scores of all documents for a particular query and method

		:return: what it returns
		:param query: describe ....
		"""
		retrieve = self.method
		#score index
		docScores = retrieve(self.query) #dict, document: score
		sortedScores = sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True) #ranked list of tuples containing docname, docscore
		topDocs = [i[0] for i in sortedScores[:20]] #create list of names of top documents
		
		return topDocs
		
		
		#you should have a good look at main2, and use the bit from '#create retrieval object'
		#on (apart from the writing part of course). You say you want to return a dictionary, but
		#you already have a sorted list with the best 50, maybe you just want to return those.
		return scores

	def createRelFreq(self, topDocs):
		"""
		calculate relative frequency for all tokens
		"""
		relFreq = dict()
		for token in self.index.index:
			for doc in topDocs:
				count = 0
				doc = doc.strip('/collection').strip('.txt')
				try:				#add relative frequency of token in document to count
					count += float(self.index.index[token][doc])/self.index.lengthOfFiles[doc] 
				except KeyError: 	#if token not in document
					pass
			for doc in self.documents:
				doc = doc.strip('collection/').strip('.txt')
				normCount = 0
				try:				#add relative frequency of token in document to normCount
					normCount += float(self.index.index[token][doc])/self.index.lengthOfFiles[doc] 
				except KeyError: 	#if token not in document
					pass
			try:
				relFreq[token] = count/normCount #doc -> relFreq
			except ZeroDivisionError:
				pass
		return relFreq


	def expandQuery(self, expansionSize = 3):
		"""
		retrieve best query expansion terms from expansionIndex and concatenate to original query
		"""

		topDocs = self.getTopDocs()
		relFreq = self.createRelFreq(topDocs)
		relFreqSorted = sorted(relFreq.iteritems(), key=operator.itemgetter(1),reverse=True) #sort by relative frequency
		expandedQuery = self.query
		#print self.query
		for n in range(expansionSize):
			expandedQuery.append(relFreqSorted[n][0])
		#print expandedQuery
			
		return expandedQuery
