class Index:
	def __init__(self):
		self.lengthOfFiles = dict()
		self.index = dict()
	"""
	very basic version of index
	Discuss what we should do here
	"""
	def createIndex(self,tokens):
		index = dict()
		for filename,words in tokens.iteritems():
			self.lengthOfFiles[filename] = len(words)
			for word in words:
				if word in index:
					if filename in index[word]:
						index[word][filename] += 1
					else:
						index[word][filename] = 1
				else:
					index[word] = dict()
					index[word][filename] = 1
		self.index = index

	
