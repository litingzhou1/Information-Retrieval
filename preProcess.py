import nltk
import itertools

#put filenames in a list
class PreProcess:

	def __init__(self, files, lancaster = False, lemmatize = False):
		self.listOfFiles = files
		self.lancaster = lancaster
		self.lemmatize = lemmatize
		self.tokens = dict()

	def makeTokens(self):
		self.tokenize()
		self.normalize()
		self.stem()
		return self.tokens

	"""
	Tokenize a list of files
	"""
	def tokenize(self):
		tokens = dict()
		for filename in self.listOfFiles:
			try:
				text = open(filename, 'r').read().decode('utf-8')
			except UnicodeDecodeError:
				text = open(filename, 'r').read().decode('iso-8859-1')
			w = [nltk.word_tokenize(t) for t in nltk.sent_tokenize(text)]
			self.tokens[filename[11:-4]] = list(itertools.chain(*w))

	"""
	Stems a list of lists of words, if Lancaster is set to true it uses Lancaster else Porter
	"""
	def stem(self):
		if self.lancaster:
			st = nltk.LancasterStemmer()
		else:
			st = nltk.PorterStemmer()

		stemmedTokens = dict()
		for filename,words in self.tokens.iteritems():
			fileStemmed = []
			for word in words:
				fileStemmed.append(st.stem(word))
			stemmedTokens[filename] = fileStemmed
		self.tokens = stemmedTokens

	"""
	If lemmatize is set to true, this function also lemmatizes
	"""
	def normalize(self):
		wnl = nltk.WordNetLemmatizer()
		normalizedTokens = dict()
		for filename,words in self.tokens.iteritems():
			fileNormalized = []
			for word in words:
				if self.lemmatize:
					word = wnl.lemmatize(word)
				fileNormalized.append(word.lower())
			normalizedTokens[filename] = fileNormalized
		self.tokens = normalizedTokens

	def filterStopwords(self):
		stopwords = nltk.corpus.stopwords.words('english')
		filteredTokens = dict()
		for filename,words in self.token.iteritems():
			fileFiltered = [w for w in words if w.lower() not in stopwords]
			filteredTokens[filename] = fileFiltered
		self.tokens = filteredTokens


