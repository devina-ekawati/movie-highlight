import nltk
import re
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import stopwords
import os
java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
os.environ['JAVAHOME'] = java_path

stopset = set(stopwords.words('english'))

depParser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

topTerm = {}

with open('imdb.txt', 'r') as text_file:
    lines = text_file.readlines()
    # text = re.sub('[^0-9a-zA-Z\s:]+', '', text)
    for text in lines:
	    dependencyTree = [list(parse.triples()) for parse in depParser.raw_parse(text)]
	    for item in dependencyTree[0]:
	    	if (item[1] == 'amod'):
	    		if item not in topTerm:
	    			topTerm[item] = 1
	    		else:
	    			topTerm[item] = topTerm[item] + 1

    # tokens=nltk.word_tokenize(str(text))
    # tokens = [w for w in tokens if not w in stopset]

print topTerm

