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
	parser.add_argument("-n", "--nopickle", help="don't use the saved (pickle) preprocessed index", action="store_true")
	parser.add_argument("-s", "--statistics", help="Print statistics about the index", action="store_true")
	parser.add_argument("-r","--retrieval", help="Specify the retrieval algorithm")
	parser.add_argument("-q","--query", help="Query string in the format <queryid> term1 term2 ... termn")
	parser.add_argument("-l", "--lemmatize", help="Lemmatize with the NLTK wordnet lemmatizer", action="store_true")
	parser.add_argument("-nl", "--nolemmatize", help="Don't lemmatize with the NLTK wordnet lemmatizer", action="store_false")
	parser.add_argument("-p", "--porter", help="Use Porter stemmer", action="store_true")
	parser.add_argument("-la", "--lancaster", help="Use Lancaster stemmer", action="store_false")
	args = parser.parse_args()

	files = glob.glob('collection/*.txt')
	documents = None if args.nopickle else loadPickle('documents.p')
	index = None if args.nopickle else loadPickle('index.p')

	ret = Retrieval(index)
	# default scoring and queries
	retrieval = {"tfidf":ret.TFIDF, "bm25": ret.BM25}
	# retrieval = {"tfidf":ret.TFIDF, "bm25 k b=": (lamda x: ret.BM25(x, k, b)}
	queries = {6: 'sustainable ecosystems', 7: 'air guitar textile sensors'}
	fname = 'out'

	if args.retrieval and args.retrieval.lower() in retrieval.keys():
		retrieval = {args.retrieval.lower() : retrieval[args.retrieval.lower()]}
		fname = args.retrieval
	if args.query:
		queries = {args.query[0] : args.query[2:]}

	# if only one of the two dual flags is used, these sets become singletons
	stemmings = set([args.porter, args.lancaster])
	lemmatizings = set([args.lemmatize, args.nolemmatize])

	with open(fname + '.txt', 'w') as f:
		for porter in stemmings:
			for lemmatizing in lemmatizings:
				if not documents:
					documents = PreProcess(files, porter, lemmatizing)
					documents.tokenize()
					documents.filterStopwords()
					documents.normalize()
					documents.stem()
					pickle.dump(documents,open('documents.p',"wb"))
				if not index:
					index = Index()
					index.createIndex(documents.tokens)
					pickle.dump(index,open('index.p',"wb"))

				if args.statistics:
					stats = Statistics()
					stats.getStatistics(documents,index)

				for retname, retrieve in retrieval.items():
					for queryid, query in queries.items():
						query = documents.stemList(documents.normalizeList(documents.filterStopwordsList(documents.tokenizeSentence(query))))
						docScores = retrieve(query)
						sortedScores = enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True))
						for rank, (doc, score) in sortedScores:
							retname += "-lemmatizing" if lemmatizing else "-nolemmatizing"
							retname += "-porter" if porter else "-lancaster"
							f.write("{0} 0 {1} {2} {3} {4}\n".format(queryid, doc, rank+1, score, retname))



