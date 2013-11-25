import nltk
import itertools
import re

#put filenames in a list
class PreProcess:

	def __init__(self, files, porter = False, lemmatize = False):
		self.listOfFiles = files
		self.lemmatize = lemmatize
		self.tokens = dict()
		self.stemmer = nltk.PorterStemmer()
		if not porter:
			self.stemmer = nltk.LancasterStemmer()
		self.wnl = nltk.WordNetLemmatizer()

	"""
	Tokenize the list of files
	"""
	def tokenize(self):
		tokens = dict()
		for filename in self.listOfFiles:
			try:
				text = open(filename, 'r').read().decode('utf-8')
			except UnicodeDecodeError:
				text = open(filename, 'r').read().decode('iso-8859-1')
			tokenizedSentences = [self.tokenizeSentence(t) for t in nltk.sent_tokenize(text)]
			self.tokens[filename[11:-4]] = list(itertools.chain(*tokenizedSentences))

	def tokenizeSentence(self, text):
		""" Tokenizes a sentence"""
		w = [token.lower() for token in nltk.word_tokenize(text)]
		# filter punctuation
		w = filter(lambda token: re.match(r'\w',token), w)
		return w

	"""
	Stems a list of lists of words, if Lancaster is set to true it uses Lancaster else Porter
	"""
	def stem(self):
		for filename,words in self.tokens.iteritems():
			self.tokens[filename] = self.stemList(words)

	def stemList(self, words):
		return [self.stemmer.stem(word) for word in words]

	"""
	If lemmatize is set to true, this function also lemmatizes
	"""
	def normalize(self):
		for filename,words in self.tokens.iteritems():
			self.tokens[filename] = self.normalizeList(words)

	def normalizeList(self, words):
		if self.lemmatize:
			words = [self.wnl.lemmatize(word) for word in words]
		return [word.lower() for word in words]

	def filterStopwords(self):
		for filename,words in self.tokens.iteritems():
			self.tokens[filename] = self.filterStopwordsList(words)

	def filterStopwordsList(self, words):
		return nltk.corpus.stopwords.words('english')
