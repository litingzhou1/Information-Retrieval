class Index:
	def __init__(self, index=dict()):
		self.lengthOfFiles = dict()
		self.index = index
	"""
	very basic version of index
	Discuss what we should do here
	"""
	def createIndex(self,tokens):
		index = dict()
		for filename,tokens in tokens.iteritems():
			self.lengthOfFiles[filename] = len(tokens)
			for token in tokens:
				if token in index:
					if filename in index[token]:
						index[token][filename] += 1
					else:
						index[token][filename] = 1
				else:
					index[token] = dict()
					index[token][filename] = 1
		self.index = index

	
