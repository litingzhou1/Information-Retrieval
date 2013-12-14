import nltk
import itertools
import re

#put filenames in a list
class PreProcess:

	def __init__(self, files, porter, lemmatize, stopwords):
		self.listOfFiles = files
		self.lemmatize = lemmatize
		self.stopwords = stopwords
		self.tokens = dict()
		self.stemmer = nltk.PorterStemmer()
		if not porter:
			self.stemmer = nltk.LancasterStemmer()
		self.wnl = nltk.WordNetLemmatizer()

		self.preProcess()

	
	def preProcess(self):
		"""	Tokenize the list of files """
		tokens = dict()
		for filename in self.listOfFiles:
			try:
				text = open(filename, 'r').read().decode('utf-8')
			except UnicodeDecodeError:
				text = open(filename, 'r').read().decode('iso-8859-1')
			self.tokens[filename[11:-4]] = self.preProcessText(text)
	
	"""
	This _one_ function is used for both document and query, to ensure valid preprocessing:
	
	* Tokenizes
	* Lowercases (normalizes)
	* Filters punctuation
	* If `stopwords` is set to true, this function does not filters stop words
	* If `lemmatize` is set to true, this function also lemmatizes
	* Stems
	
	"""
	def preProcessText(self, text):
		# tokenize words and sentences and normalize
		words = [token.lower() for sentence in nltk.sent_tokenize(text) for token in nltk.word_tokenize(sentence)]
		# filter punctuation
		words = filter(lambda token: re.match(r'\w',token), words)
		# filter stopwords
		if not self.stopwords:
			words = filter(lambda token: token not in nltk.corpus.stopwords.words('english'), words)
		# lemmatize
		if self.lemmatize:
			words = [self.wnl.lemmatize(word) for word in words]
		# stem using `self.stemmer`
		words = [self.stemmer.stem(word) for word in words]
		return words
