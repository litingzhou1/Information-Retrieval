Information Retrieval
=====================
with TREC evaluation output

Usage
-----

```
  usage: main.py [-h] [-n] [-s] [-l] [-sw] [-st {porter,lancaster}]
                  [-r {tfidf,bm25}] [-q QUERY] [-qe] [-a] [-o OUTPUT]

  optional arguments:
    -h, --help            show this help message and exit
    -n, --noPickle        don't use the saved (pickle) preprocessed index
    -s, --statistics      Print statistics about the index
    -l, --lemmatize       Lemmatize with the NLTK wordnet lemmatizer
    -sw, --stopwords      Include stopwords
    -st {porter,lancaster}, --stemmer {porter,lancaster}
                          Specify stemmer
    -r {tfidf,bm25}, --retrieval {tfidf,bm25}
                          Specify the retrieval algorithm
    -q QUERY, --query QUERY
                          Query string in the format <queryid> term1 term2 ...
                          termn
    -qe, --queryExpansion
                          Use Query Expansion
    -a, --all             Retrieve with all lemmatizing, stemmers, queries, and
                          retrieval methods
    -o OUTPUT, --output OUTPUT
                          Specify output file
```

Dependencies
------------
nltk
