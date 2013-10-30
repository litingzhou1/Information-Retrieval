from preProcess import PreProcess
from index import Index

if __name__ == "__main__":
	words = PreProcess()
	words.tokenize()
	words.normalize()
	words.stem()

	
	index = Index()
	invindex = index.createIndex(words.tokens)
	print invindex

