from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
from statistics import Statistics
import cPickle as pickle
import glob
import argparse
import operator

def loadPickle(fname):
	""" If `nopickle` is true or loading from `fname` failes, run `buildfunc`  """
	try:
		with open(fname) as f:
			return pickle.load(f)
	except IOError:
		return None

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("--index", help="provide pickled index file", default = None)
	parser.add_argument("--preprocess", help = "provide pickled preprocess file", default = None)
	parser.add_argument("-n", "--nopickle", help="don't use the saved (pickle) preprocessed index", action="store_true")
	parser.add_argument("-s", "--statistics", help="Print statistics about the index", action="store_true")
	parser.add_argument("-r","--retrieval", default ='tfidf', type = str.lower, choices = ['tfidf','bm25'], help="Specify the retrieval algorithm")
	parser.add_argument("-q","--query", default = '6 sustainable ecosystems', help="Query string in the format <queryid> term1 term2 ... termn")
	parser.add_argument("-l", "--lemmatize", help="Lemmatize with the NLTK wordnet lemmatizer", default = False, action="store_true")
	parser.add_argument("-st", "--stemmer", help="Specify stemmer", default = 'porter', type = str.lower, choices = ['porter', 'lancaster'])
	parser.add_argument("-o", "--output", help="Specify output file", default = 'output')
	
	args = parser.parse_args()

	files = glob.glob('collection/*.txt')
	f = open(args.output + '.txt','w')

	#format query
	query_list = args.query.split()
	query_id, query = query_list[0], ' '.join(query_list[1:])

	#preprocessing
	if not args.preprocess:
		print 'Preprocessing'
		lem, stem = args.lemmatize, args.stemmer
		print 'Lemmatizing: %s\t stemming: %s' % (lem, stem)
		documents = PreProcess(files, stem == 'porter', lem)
		documents.tokenize()
		documents.filterStopwords()
		documents.normalize()
		documents.stem()
		fname = 'documents_lem=%s_stem=%s.p' % (lem, stem)
		pickle.dump(documents,open(fname,"wb"))
		print 'Preprocessing object pickled to %s\n' % fname
	else:
		documents = loadPickle(args.preprocess)

	#create index
	if not args.index:
		print "Creating index"
		index = Index()
		index.createIndex(documents.tokens)
		fname = 'index_lem=%s_stem=%s.p' % (lem, stem)
		pickle.dump(index,open(fname,"wb"))
		print 'Preprocessing object pickled to %s\n' % fname
	else:
		index = loadPickle(args.index)

	#print statistics if required
	if args.statistics:
		stats = Statistics()
		stats.getStatistics(documents, index)

	#create retrieval object
	retrieving = Retrieval(index)
	retrieval_dict = {'tfidf': retrieving.TFIDF, 'bm25': retrieving.BM25}
	retrieve = retrieval_dict[args.retrieval]

	#score index and write to file
	query = documents.stemList(documents.normalizeList(documents.filterStopwordsList(documents.tokenizeSentence(query))))
	docScores = retrieve(query)
	sortedScores = enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True))
	for rank, (doc, score) in sortedScores:
		f.write("{0} 0 {1} {2} {3}\n".format(query_id, doc, rank+1, score))



