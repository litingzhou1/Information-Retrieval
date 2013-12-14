from math import log

class PLM:
	def __init__(self,amountOfTokens,lam=0.5):
		self.amountOfTokens = amountOfTokens
		#Set the lambda used in computing the E-step in EM-maximization
		self.lam = lam


	""" Perform an EM maximization step  """
	def parsimony(self,index, plm):
		for token in index:
			for document in index[token]:
				if document == "cf":
					continue
				# This try-except is necessary for initializing the plm
				try:
					ptD = plm[token][document] 
				except KeyError:
					ptD = 0.1
				tC = float(index[token]["cf"]) / self.amountOfTokens
				e = (index[token][document] * self.lam * ptD) / ((1-self.lam)*tC + self.lam*ptD)
				if plm.get(token):
					plm[token].update({document: e})
				else:
					plm[token] = {document: e}



		""" compute P(t|D) by normalizing e """
		for token in index:
			totalE = sum(plm[token].values())
			for document in index[token]:
				if document == "cf":
					continue;
				plm[token][document] = plm[token][document] / float(totalE)

		return plm

	" Compute score for PLM"""
	def score(self, query, index, plm):
		CE = dict()
		print "modelling the query"
		for i in range(1,10):	
			for token in query:
				for document in index[token]:
					if document == "cf":
						continue
					# This try-except is necessary for initializing the plm
					try:
						ptR = CE[token][document] 
					except KeyError:
						ptR = 0.1
					tC = float(index[token]["cf"]) / self.amountOfTokens
					e = query.count(token) * (self.lam * ptR) / ((1-self.lam)*tC + self.lam*ptR)
					if CE.get(token):
						CE[token].update({document: e})
					else:
						CE[token] = {document: e}



			""" compute P(t|R) by normalizing e """
			for token in query:
				totalE = sum(CE[token].values())
				for document in index[token]:
					if document == "cf":
						continue;
					CE[token][document] = CE[token][document] / float(totalE)

		
		score = dict()
		#Take the documents in which all query terms appear
		docs = set.intersection(*[set(plm[term].keys()) for term in query])
		docs.discard("cf")
		for term in query:
			for doc in plm[term]:
				tC = float(index[token]["cf"]) / self.amountOfTokens
				if score.get(doc):
					score[doc] -= CE[term][doc]*log((1-self.lam) * tC + self.lam* plm[term][doc]) 
				else:
					score[doc] = -CE[term][doc]*log((1-self.lam) * tC + self.lam* plm[term][doc]) 
		return score		


