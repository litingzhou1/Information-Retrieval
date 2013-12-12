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

		:Input: self (containing query and method)
		:Returns: the top 20 documents for the query, using the method specified
		"""
		retrieve = self.method
		#score index
		docScores = retrieve(self.query) #dict, document: score
		sortedScores = sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True) #ranked list of tuples containing docname, docscore
		topDocs = [i[0] for i in sortedScores[:20]] #create list of names of top documents
		
		return topDocs

	def createRelFreq(self, topDocs):
		"""
		# calculate relative frequency for all tokens

		:Input: self and best 20 documents for query and method 
		:Returns:
		"""
		relFreq = dict()
		absFreq = dict()
		for token in self.index.index:
			countAbs = 0
			count = 0
			for doc in topDocs:
				doc = doc.strip('/collection').strip('.txt')
				try:				#add relative frequency of token in document to count
					count += float(self.index.index[token][doc])/self.index.lengthOfFiles[doc] 
					#add number of times token is in document
					countAbs += float(self.index.index[token][doc])
				except KeyError: 	#if token not in document
					pass

			relFreq[token] = count #doc -> relFreq
			#calculate absFreq = total occurrences in topdocs/total in all docs
			absFreq[token] = countAbs
	
		return relFreq, absFreq


	def expandQuery(self, expansionSize = 10):
		"""
		retrieve best query expansion terms from expansionIndex and concatenate to original query
		For relative frequencies, frequency in each document is divided by frequency in all docs
		For absolute frequencies, frequency in all topdocs is divided by frequency in all docs
		"""

		topDocs = self.getTopDocs()
		relFreq, absFreq = self.createRelFreq(topDocs)
		relFreqSorted = sorted(relFreq.iteritems(), key=operator.itemgetter(1),reverse=True) #sort by relative frequency
		absFreqSorted = sorted(absFreq.iteritems(), key=operator.itemgetter(1),reverse=True) #sort by absolute frequency
		expandedQueryRel = self.query
		expandedQueryAbs = self.query

		for n in range(expansionSize):
			#append token with highest
			if relFreqSorted[n][0] not in self.query:
				expandedQueryRel.append(relFreqSorted[n][0])
			if absFreqSorted[n][0] not in self.query:
				expandedQueryAbs.append(absFreqSorted[n][0])

		#print 'rel: ', expandedQueryRel
		#print 'abs: ', expandedQueryAbs	

		return expandedQueryRel, expandedQueryRel
