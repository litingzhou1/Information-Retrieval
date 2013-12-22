from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
from statistics import Statistics
from queryExpansion import QueryExpansion
from PLM import PLM
from wordvec import WordVector

import cPickle as pickle
import glob
import argparse
import operator

def loadPickleOrCreate(fname, create, noPickle):
	""" If `noPickle` or loading from `fname` failes, run `create`  """
	if noPickle:
		out = create()
		print 'Pickling %s' % fname
		pickle.dump(out,open(fname,"wb"))
		return out
	try:
		with open(fname) as f:
			print "using pickled file"
			return pickle.load(f)
	except IOError:
		return loadPickleOrCreate(fname,create,True)

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
	parser.add_argument("-l", "--lemmatize", help="Lemmatize with the NLTK wordnet lemmatizer", default = False, action="store_true")
	parser.add_argument("-sw", "--stopwords", help="Keep stopwords", default = False, action="store_true")
	parser.add_argument("-st", "--stemmer", help="Specify stemmer", default = 'porter', type = str.lower, choices = ['porter', 'lancaster'])
	parser.add_argument("-q","--query", help="Query string in the format <queryid> term1 term2 ... termn")
	parser.add_argument("-qe", "--queryExpansion", help="Specify Query Expansion", default = False, type = str.lower, choices = ['abs','rel'])
	parser.add_argument("-m","--model", help="Select model" , default="tfidf", type = str.lower, choices = ['tfidf','bm25','plm','tfcosine'])
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
			if args.query:
				query_list = args.query.split()
				queries = {query_list[0]: ' '.join(query_list[1:])}
			else:
				queries = {6: 'sustainable ecosystems', 7: 'air guitar textile sensors'}

			# make documents, index and retrieval objects for this stemmer and lemmatizing stettings
			documents, index = indexDocuments(files, args.noPickle, args.lemmatize, args.stemmer, args.stopwords)
			retrieving = Retrieval(index)

			#If PLM, then compute the PLM before retrieval
			if args.model == "plm":
				print "Training PLM"
				amountOfTokens = sum(map(len,documents.tokens.values()))
				plm = PLM(amountOfTokens)
				plmIndex = plm.parsimony(index.index,dict())
				#Repeat EM 10 times, can be changed as necessary
				for i in range(0,10):
					plmIndex = plm.parsimony(index.index,plmIndex)

			#If TFcosine, then build the document vectors before retrieval
			if args.model == "tfcosine":
				print "Building document vectors"
				wordvec = WordVector(index, documents.tokens)


			for queryID, queryString in queries.iteritems():
				# Preprocess queries
				query = documents.preProcessText(queryString)

				#Create expanded queries
				if args.queryExpansion:
					print "Adding terms with query expansion"
					query = documents.preProcessText(queryString)
					expansionObject = QueryExpansion(index, documents, query, retrieving.BM25)
					absQ, relQ = expansionObject.expandQuery()
					if args.queryExpansion == "rel":
						query = relQ
					else:
						query = absQ

				print "Retrieving scores for: "
				print query

				# Retrieve all scores and write them to file
				if args.model == "plm":
					docScores = plm.score(query,index.index, plmIndex)
				elif args.model == "tfidf":
					docScores = retrieving.TFIDF(query)
				elif args.model == "bm25":
					docScores = retrieving.BM25(query)
				elif args.model == "tfcosine":
					docScores = wordvec.cosine(query)
				
				sortedScores = enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True))
				name = 'l=%s_st=%s_sw=%s_r=%s_qe=%s' % (args.lemmatize, args.stemmer, args.stopwords, args.model, args.queryExpansion)
				for rank, (doc, score) in sortedScores:
					f.write("{0} 0 {1} {2} {3} {4}\n".format(queryID, doc, rank+1, score, name))
