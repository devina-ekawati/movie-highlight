import nltk
import re
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import operator
import os

java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
os.environ['JAVAHOME'] = java_path

depParser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

topTerm = {}

with open('rottentomatoes.txt', 'r') as text_file:
    lines = text_file.readlines()
    for text in lines:
    	sentences = sent_tokenize(text.strip())
    	for sentence in sentences:
	    dependencyTree = [list(parse.triples()) for parse in depParser.raw_parse(sentence)]
	    for item in dependencyTree[0]:
	    	if (item[1] == 'amod'):
	    		newitem = (item[0][0],item[2][0])
	    		if newitem not in topTerm:
	    			topTerm[newitem] = 1
	    		else:
	    			topTerm[newitem] = topTerm[newitem] + 1

topTerm = sorted(topTerm.items(), key=operator.itemgetter(1))[-10:]

listTopReviews = []

for term in topTerm:
	string = term[0][1] + " " + term[0][0]
	listTopReviews.append(string)

seq = {key: [] for key in listTopReviews}

for line in lines:
	for highlight in listTopReviews:
		tmp = highlight.split(" ")
		if (tmp[0] in line and tmp[1] in line):
			seq[highlight].append(line)

print seq
# print "\n"

# for highlight in listTopReviews:
# 	print highlight + "\n"
# 	for review in seq[highlight]:
# 		print review
