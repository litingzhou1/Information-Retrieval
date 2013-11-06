from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
import cPickle as pickle
import glob
import argparse

def loadPickle(fname, buildfunc, nopickle):
	""" If `nopickle` is true or loading from `fname` failes, run `buildfunc`  """
	if nopickle:
		return buildfunc()
	try:
		with open(fname) as f:
			return pickle.load(f)
	except IOError:
		b =  buildfunc()
		pickle.dump(b ,open(fname,"wb"))
		return b
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--nopickle", help="don't use the saved (pickle) preprocessed index", action="store_true")
	args = parser.parse_args()

	files = glob.glob('collection/*.txt')
	words = PreProcess(files)
	index = Index()

	words.tokens = loadPickle('tokens.p', lambda: words.createTokens(), args.nopickle)
	index.index = loadPickle('index.p', lambda: index.createIndex(words.tokens) , args.nopickle)

	ret = Retrieval(index.index, len(files))
	print ret.TFIDF([u'a'])


