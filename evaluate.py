import subprocess
import sys

'''
This file is a placeholder for a better implementation, just used to try out trec_eval
'''

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print "Please input a filename"
		sys.exit()
	#If you want to run it manually, use this line in the console for TFIDF
	#./trec_eval -q -M262 qrels.txt TFIDF.txt
	subprocess.call(["./trec_eval", "-q","-M262", "qrels.txt", str(sys.argv[1])])
