from preProcess import PreProcess
from index import Index
from retrieval import Retrieval
import cPickle as pickle
import glob

if __name__ == "__main__":
	files = glob.glob('collection/*.txt')
	words = PreProcess(files)
	try:
		with open('tokens.p') as tokenfile:
			words.tokens = pickle.load(tokenfile)
	except IOError:
		words.tokenize()
		words.normalize()
		words.stem()
		pickle.dump(words.tokens,open("tokens.p","wb"))

	
	index = Index()
	try:
		with open('index.p') as indexfile:
			index.index = pickle.load(indexfile)
	except IOError:
		index.createIndex(words.tokens)
		pickle.dump(index.index,open("index.p","wb"))

	ret = Retrieval(index.index, len(files))
	print ret.TFIDF([u'a'])

	

