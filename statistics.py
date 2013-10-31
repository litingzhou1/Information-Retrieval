from preProcess import PreProcess
from index import Index
import cPickle as pickle

if __name == "__main__":
	words = PreProcess()
	try:
		with open('tokens.p') as tokenfile:
			words.tokens = pickle.load(tokenfile)
	except IOError:
		words.tokenize()
		# words.normalize()
		# words.stem()
		pickle.dump(words.tokens,open("tokens.p","wb"))

	index = Index()
	try:
		with open('index.p') as indexfile:
			index.index = pickle.load(indexfile)
	except IOError:
		index.createIndex(words.tokens)
		pickle.dump(index.index,open("index.p","wb"))

	print "Total number of tokens: %i" % sum(words.tokens.values())
	print "Total number of unique tokens %i" % len(index.index)
	print "Total number of unique tokens %i" % sum(index["of"].values())



