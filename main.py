from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
import cPickle as pickle
import glob
import argparse

def loadPickle(fname, nopickle):
	""" If `nopickle` is true or loading from `fname` failes, run `buildfunc`  """
	if nopickle:
		return None
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
	words = PreProcess(files,loadPickle('tokens.p',args.nopickle))
	index = Index(loadPickle('index.p',args.nopickle))

	if not words.tokens: 
		words.tokenize()
		words.normalize()
		words.stem()
	if not index.index:
		index.createIndex(words.tokens)

	ret = Retrieval(index.index, len(files))
	print ret.TFIDF([u'a'])


