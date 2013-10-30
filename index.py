class Index:
	"""
	very basic version of index
	Does not include frequency of occurence, instead keeps appending its ID to the filelist.

	Discuss what we should do here
	"""
	def createIndex(self,tokens):
		index = dict()
		for filename,line in tokens.iteritems():
			for word in line:
				if word in index:
					index[word][0] += 1
					index[word][1].append(filename)
				else:
					index[word] = []
					index[word].append(1)
					index[word].append([filename])
		return index

	
