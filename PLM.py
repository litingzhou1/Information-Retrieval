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
					e = plm[token][document] 
				except KeyError:
					e = 0.1
				tC = float(index[token]["cf"]) / self.amountOfTokens
				e = (index[token][document] * self.lam * e) / ((1-self.lam)*tC + self.lam*e)
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

