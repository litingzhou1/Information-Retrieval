import nltk
import itertools

#put filenames in a list
class PreProcess:

	def __init__(self, files, lancaster = False, lemmatize = False):
		self.listOfFiles = files

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
			tokens[filename[11:-4]] = list(itertools.chain(*w))
			#Filter out punctuation
			for filename,tokens in self.tokens.iteritems():
				tokens[filename] = filter(lambda token: token not in ',-()', tokens)
			return tokens;

	"""
	Stems a list of lists of words, if Lancaster is set to true it uses Lancaster else Porter
	"""
	def stem(self,tokens, lancaster = True):
		if lancaster:
			st = nltk.LancasterStemmer()
		else:
			st = nltk.PorterStemmer()

		stemmedTokens = dict()
		for filename,words in tokens.iteritems():
			fileStemmed = []
			for word in words:
				fileStemmed.append(st.stem(word))
			stemmedTokens[filename] = fileStemmed
		self.tokens = stemmedTokens

	"""
	If lemmatize is set to true, this function also lemmatizes
	"""
	def normalize(self,tokens):
		wnl = nltk.WordNetLemmatizer()
		normalizedTokens = dict()
		for filename,words in tokens.iteritems():
			fileNormalized = []
			for word in words:
				if self.lemmatize:
					word = wnl.lemmatize(word)
				fileNormalized.append(word.lower())
			normalizedTokens[filename] = fileNormalized
		return normalizedTokens

	def filterStopwords(self,tokens):
		stopwords = nltk.corpus.stopwords.words('english')
		filteredTokens = dict()
		for filename,words in tokens.iteritems():
			fileFiltered = [w for w in words if w.lower() not in stopwords]
			filteredTokens[filename] = fileFiltered
		return filteredTokens


