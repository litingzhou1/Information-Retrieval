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
	args = parser.parse_args()

	files = glob.glob('collection/*.txt')
	documents = None if args.nopickle else loadPickle('documents.p')
	index = None if args.nopickle else loadPickle('index.p')

	if not documents: 
		documents = PreProcess(files)
		documents.tokenize()
		# documents.normalize()
		# documents.stem()
		pickle.dump(documents,open('documents.p',"wb"))
	if not index:
		index = Index()
		index.createIndex(documents.tokens)
		pickle.dump(index,open('index.p',"wb"))

	if args.statistics:
		stats = Statistics()
		stats.getStatistics(documents,index)

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

	with open(fname + '.txt', 'w') as f:
		for retname, retrieve in retrieval.items():
			for queryid, query in queries.items():
				docScores = retrieve(query.split())
				sortedScores = enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1),reverse=True))
				for rank, (doc, score) in sortedScores:
					f.write("{0} 0 {1} {2} {3} {4}\n".format(queryid, doc, rank+1, score, retname))



