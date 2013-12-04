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
	parser.add_argument("-r","--retrieval", default ='tfidf', type = str.lower, choices = ['tfidf','bm25'], help="Specify the retrieval algorithm")
	parser.add_argument("-q","--query", default = '6 sustainable ecosystems', help="Query string in the format <queryid> term1 term2 ... termn")
	parser.add_argument("-qe", "--queryExpansion", help="Specify Query Expansion", default = None, choices = ['abs','rel'])
	parser.add_argument("-plm","--parsimoniousLM", help="Use PLM", action="store_true")
	parser.add_argument("-a", "--all", help="Retrieve with all lemmatizing, stemmers, queries, and retrieval methods", action="store_true")
	parser.add_argument("-o", "--output", help="Specify output file", default = 'output')
	
	args = parser.parse_args()
	files = glob.glob('collection/*.txt')

	if args.statistics:
		# print statistics if required
		documents, index = indexDocuments(files, args.noPickle, args.lemmatize, args.stemmer, True)
		stats = Statistics()
		stats.getStatistics(documents, index)
	else:
		# write query results to output document, 
		with open(args.output + '.txt', 'w') as f:
			if args.all:
				queries = {6: 'sustainable ecosystems', 7: 'air guitar textile sensors'}
			else:
				query_list = args.query.split()
				queries = {query_list[0]: ' '.join(query_list[1:])}

			# loop over specified stop word filtering, lemmatizing, stemmers, queries, and retrieval methods
			for stopwords in [True, False] if args.all else [args.stopwords]:
				for lemmatize in [True, False] if args.all else [args.lemmatize]:
					for stemmer in ['porter', 'lancaster'] if args.all else [args.stemmer]:
						# make documents, index and retrieval objects for this stemmer and lemmatizing stettings
						documents, index = indexDocuments(files, args.noPickle, lemmatize, stemmer, stopwords)
						retrieving = Retrieval(index)
						retrievalDict = {'tfidf': retrieving.TFIDF, 'bm25': retrieving.BM25}
						for queryID, queryString in queries.iteritems():
							# make query term list from query string
							query = documents.preProcessText(queryString)
							if PLM:
								amountOfTokens = sum(map(len,documents.tokens.values()))
								plm = PLM(amountOfTokens)
								plmIndex = plm.parsimony(index.index,dict())
								for i in range(0,10):
									plmIndex = plm.parsimony(index.index,plmIndex)

								score = plm.retrieval(query,plmIndex)
								print score
							for retrieval, retrieve in retrievalDict.iteritems() if args.all else [(args.retrieval, retrievalDict[args.retrieval])]:
								for queryExpansion in [None, 'abs', 'rel'] if args.all else [args.queryExpansion]:
									

									# expand query
									if queryExpansion:
										expansionObject = QueryExpansion(index, documents, query, retrieve)
										absQ, relQ = expansionObject.expandQuery()
										query = absQ if queryExpansion == 'abs' else relQ

									# Retrieve all scores and write them to file
									docScores = retrieve(query)
									sortedScores = enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True))
									name = 'l=%s_st=%s_sw=%s_r=%s_qe=%s' % (lemmatize, stemmer, stopwords, retrieval, queryExpansion)
									for rank, (doc, score) in sortedScores:
										f.write("{0} 0 {1} {2} {3} {4}\n".format(queryID, doc, rank+1, score, name))
