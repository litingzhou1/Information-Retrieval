from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
from statistics import Statistics
from queryExpansion import QueryExpansion
from PLM import PLM

import cPickle as pickle
import glob
import argparse
import operator

def loadPickleOrCreate(fname, create, noPickle):
	""" If `noPickle` or loading from `fname` failes, run `create`  """
	try:
		with open(fname) as f:
			print "using pickled file"
			return pickle.load(f)
	except IOError:
		noPickle = True
	if noPickle:
		out = create()
		print 'Pickling %s' % fname
		pickle.dump(out,open(fname,"wb"))
		return out

def indexDocuments(files, noPickle, lem, stem, sw):
	""" Build a document and an index object with specified preprocessing, or possibly load it from a pickle if that exists """
	print 'Creating index [--lemmatize=%s --stemmer=%s --stopwords=%s]' % (lem,stem,sw)

	# open or load documents
	fname = 'documents_l=%s_st=%s_sw=%s.p' % (lem, stem, sw)
	create = lambda: PreProcess(files, stem == 'porter', lem, sw)
	documents = loadPickleOrCreate(fname, create, noPickle)

	# open or load index
	fname = 'index_l=%s_st=%s_sw=%s.p' % (lem, stem, sw)
	create = lambda: Index(documents.tokens)
	index = loadPickleOrCreate(fname, create, noPickle)

	return documents, index

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--noPickle", help="don't use the saved (pickle) preprocessed index", action="store_true")
	parser.add_argument("-s", "--statistics", help="Print statistics about the index", action="store_true")
	parser.add_argument("-l", "--lemmatize", help="Lemmatize with the NLTK wordnet lemmatizer", default = True, action="store_true")
	parser.add_argument("-sw", "--stopwords", help="Keep stopwords", default = False, action="store_true")
	parser.add_argument("-st", "--stemmer", help="Specify stemmer", default = 'porter', type = str.lower, choices = ['porter', 'lancaster'])
	parser.add_argument("-q","--query", help="Query string in the format <queryid> term1 term2 ... termn")
	parser.add_argument("-qe", "--queryExpansion", help="Specify Query Expansion", action = "store_true", default = False)
	parser.add_argument("-plm","--parsimoniousLM", help="Use PLM", action="store_true", default = False)
	
	args = parser.parse_args()
	files = glob.glob('collection/*.txt')

	if args.statistics:
		# print statistics if required
		documents, index = indexDocuments(files, args.noPickle, args.lemmatize, args.stemmer, True)
		stats = Statistics()
		stats.getStatistics(documents, index)
	else:
		# write query results to output document, 
		with open('output.txt', 'w') as f:
			if args.query:
				query_list = args.query.split()
				queries = {query_list[0]: ' '.join(query_list[1:])}
			else:
				queries = {6: 'sustainable ecosystems', 7: 'air guitar textile sensors'}

			# make documents, index and retrieval objects for this stemmer and lemmatizing stettings
			documents, index = indexDocuments(files, args.noPickle, args.lemmatize, args.stemmer, args.stopwords)
			retrieving = Retrieval(index)
			retrievalDict = {'tfidf': retrieving.TFIDF, 'bm25': retrieving.BM25}

			#If PLM, then compute the PLM before retrieval
			if args.parsimoniousLM:
				print "Training PLM"
				retrievalDict["plm"] = retrieving.PLM
				amountOfTokens = sum(map(len,documents.tokens.values()))
				plm = PLM(amountOfTokens)
				plmIndex = plm.parsimony(index.index,dict())
				#Repeat EM 10 times, can be changed as necessary
				for i in range(0,10):
					plmIndex = plm.parsimony(index.index,plmIndex)

			del retrieving.index["cf"]


			#Add expanded queries to the list
			if args.queryExpansion:
				print "Adding queries with query expansion"
				vanillaqueries = queries
				for queryID,queryString in vanillaqueries.iteritems():
					expansionObject = QueryExpansion(index, documents, query, retrieve)
					absQ, relQ = expansionObject.expandQuery()
					queries[queryID+10] = absQ
					queries[queryID+100] = relQ
							

			for queryID, queryString in queries.iteritems():
				# Preprocess queries
				query = documents.preProcessText(queryString)
				print "Retrieving scores for: "
				print query
				for retrieval, retrieve in retrievalDict.iteritems():
						# Retrieve all scores and write them to file
						if PLM and retrieval == "plm":
							docScores = retrieve(query,plmIndex)
						else:
							docScores = retrieve(query)
						sortedScores = enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True))
						name = 'l=%s_st=%s_sw=%s_r=%s_qe=%s' % (args.lemmatize, args.stemmer, args.stopwords, retrieval, args.queryExpansion)
						for rank, (doc, score) in sortedScores:
							f.write("{0} 0 {1} {2} {3} {4}\n".format(queryID, doc, rank+1, score, name))
