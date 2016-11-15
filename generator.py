import nltk
import re
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import operator
import os

java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
os.environ['JAVAHOME'] = java_path

stopset = set(stopwords.words('english'))

depParser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

topTerm = {}

with open('rottentomatoes.txt', 'r') as text_file:
    lines = text_file.readlines()
    # text = re.sub('[^0-9a-zA-Z\s:]+', '', text)
    for text in lines:
    	sentences = sent_tokenize(text.strip())
    	for sentence in sentences:
	    dependencyTree = [list(parse.triples()) for parse in depParser.raw_parse(sentence)]
	    for item in dependencyTree[0]:
	    	if (item[1] == 'amod'):
	    		if item not in topTerm:
	    			topTerm[item] = 1
	    		else:
	    			topTerm[item] = topTerm[item] + 1

topTerm = sorted(topTerm.items(), key=operator.itemgetter(1))[-10:]

listTopTerm = []

for term in topTerm:
	string = term[0][2][0] + " " + term[0][0][0]
	print string

print topTerm

