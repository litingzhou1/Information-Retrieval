Benno Kruit - 10576223
Joost van Amersfoort - 10021248 
Otto Fabius - 5619858

usage: main.py [-h] [-n] [-s] [-l] [-sw] [-st {porter,lancaster}] [-q QUERY]
               [-qe] [-m {tfidf,bm25,plm}] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -n, --noPickle        don't use the saved (pickle) preprocessed index
  						(if none is found, a new one is created anyway)
  -s, --statistics      Print statistics about the index
  						(for the intermediary deadline)
  -l, --lemmatize       Lemmatize with the NLTK wordnet lemmatizer
  -sw, --stopwords      Keep stopwords, default is to filter stopwords
  -st {porter,lancaster}, --stemmer {porter,lancaster}
                        Specify stemmer, default is porter.
  -q QUERY, --query QUERY
                        Query string in the format <queryid> term1 term2 ...
						Default is "6 Sustainable environment" and "7 air guitar textile sensors"
  -qe {abs,rel}, --queryExpansion {abs,rel}
                         Specify Query Expansion
  -m {tfidf,bm25,plm}, --model {tfidf,bm25,plm}
                        Select model
						Default is TF-IDF
  -o OUTPUT, --output OUTPUT
                        Specify output file (.txt is appended to the filename chosen)
					

Example:

>> python main.py -m tfidf -o tfidf

Will create an index (porter stemmer, filter stopwords) if no pickles are found, then run tfidf with the default queries and save a file called tfidf.txt with the output.

This output can directly be read into the trec_eval program:

>> ./trec_eval -q -M1000 qrels.txt tfidf.txt


NOTE:
The program expects a folder called collection at the same level as main. 





