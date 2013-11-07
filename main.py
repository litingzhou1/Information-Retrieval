from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
from statistics import Statistics
import cPickle as pickle
import glob
import argparse

def loadPickle(fname):
	""" Load pickle variable, except if loading from `fname` failes, then return None  """
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
	documents = PreProcess(files) if args.nopickle else loadPickle('documents.p')
	index = Index() if args.nopickle else loadPickle('index.p')

	if not documents.tokens: 
		documents.tokenize()
		documents.normalize()
		documents.stem()
		pickle.dump(documents,open('documents.p',"wb"))
	if not index.index:
		index.createIndex(documents.tokens)
		pickle.dump(index,open('index.p',"wb"))

	if args.statistics:
		stats = Statistics()
		stats.getStatistics(documents,index)

	if args.retrieval.lower() == "tfidf":
		ret = Retrieval(index)
		print ret.TFIDF([u'sustainable',u'ecosystems'])


