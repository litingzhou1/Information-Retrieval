from math import log

class PLM:
	def __init__(self,amountOfTokens,lam=0.5):
		self.amountOfTokens = amountOfTokens
		self.lam = lam


	def parsimony(self,index, plm):
		for token in index:
			for document in index[token]:
				if document == "cf":
					continue
				try:
					e = plm[token][document] 
				except KeyError:
					e = 0.1
				tC = float(index[token]["cf"]) / self.amountOfTokens
				e = (index[token][document] * self.lam * e) / ((1-self.lam)*tC + self.lam*e)
				if plm.get(token):
					plm[token].update({document: e})
				else:
					plm[token] = {document: e}



		for token in index:
			totalE = sum(plm[token].values())
			for document in index[token]:
				if document == "cf":
					continue;
				plm[token][document] = plm[token][document] / float(totalE)

		return plm

	def retrieval(self, query, plm):
		score = dict()
		#This should work, but it doesn't
		docs = set.intersection(*[set(plm[term].keys()) for term in query])
		for term in query:
			for doc in plm[term]:
				if score.get(doc):
					score[doc] += log(plm[term][doc])
				else:
					score[doc] =  log(plm[term][doc])
			
		return score		


