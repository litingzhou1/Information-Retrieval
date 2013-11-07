from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
from statistics import Statistics
import cPickle as pickle
import glob
import argparse

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
	parser.add_argument("-r","--retrieval", help="Specify the retrieval algorithm", default="TFIDF")
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

	if args.retrieval.lower() == "tfidf":
		ret = Retrieval(index)
		with open(args.retrieval+'.txt', 'w') as f:
			# run query number 6
			docScores = ret.TFIDF('sustainable ecosystems'.split())
			for rank, (doc, score) in enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1))):
				f.writeline("6 0 {0} {1} {2} {3}".format(doc, rank, score, args.retrieval))

			# run query number 7
			docScores = ret.TFIDF('air guitar textile sensors'.split())
			for rank, (doc, score) in enumerate(sorted(docScores.iteritems(), key=operator.itemgetter(1))):
				f.writeline("7 0 {0} {1} {2} {3}".format(doc, rank, score, args.retrieval))



