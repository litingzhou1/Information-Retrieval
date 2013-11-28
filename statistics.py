class Statistics():
	def getStatistics(self,documents,index):
		print "Total number of tokens: %i" % sum(map(len,documents.tokens.values()))
		print "Total number of unique tokens %i" % len(index.index)
		print "Total number of occurences of 'of' %i" % (sum(index.index["of"].values()) if "of" in index.index else 0)
	



