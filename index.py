class Index:
	def __init__(self, docs):
		self.lengthOfFiles = dict()
		self.index = dict()

		for filename,tokens in docs.iteritems():
			self.lengthOfFiles[filename] = len(tokens)
			for token in tokens:
				if token in self.index:
					if filename in self.index[token]:
						self.index[token][filename] += 1
					else:
						self.index[token][filename] = 1
				else:
					self.index[token] = dict()
					self.index[token][filename] = 1		

		for token in self.index:
			self.index[token]["cf"] = sum(self.index[token].values())


	
