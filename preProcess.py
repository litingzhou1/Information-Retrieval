from __future__ import division
import glob
import nltk
import re

#put filenames in a list
listOfFiles = glob.glob('./collection/*.txt')

# stemming function, could also use porter or Lancaster stemmer
def stem(word):
    regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
    s, suffix = re.findall(regexp, word)[0]
    return s

#create dict, key = filename, value = bag of words
files = dict()
tokens = dict()
stemmedTokens = dict()
freqDist = dict()
# first tokenize, then lower and stem:
for file in range(len(listOfFiles)):
	text = open(listOfFiles[file])
	filename = listOfFiles[file]
	tokens[filename] = nltk.word_tokenize(text.read())
	stemmedTokens[filename] = [stem(t.lower()) for t in tokens[filename]]
	print file #for progress
	#Now create dictionary of frequency distributions of words:

	# nltk.FreqDis(t) for t in stemmedTokens[filename]


#example: 
# print stemmedTokens['./collection/CSIRO084-05928091.txt']

