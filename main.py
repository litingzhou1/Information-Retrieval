from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
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
	args = parser.parse_args()

	files = glob.glob('collection/*.txt')
	words = PreProcess(files) if args.nopickle else loadPickle('words.p')
	index = Index() if args.nopickle else loadPickle('index.p')

	if not words.tokens: 
		words.tokenize()
		words.normalize()
		words.stem()
		pickle.dump(words,open('words.p',"wb"))
	if not index.index:
		index.createIndex(words.tokens)
		pickle.dump(index,open('index.p',"wb"))

	ret = Retrieval(index)
	print ret.BM25([u'a'])


