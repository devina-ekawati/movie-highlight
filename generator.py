import nltk
import re
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import stopwords

stopset = set(stopwords.words('english'))

with open('all_review.txt', 'r') as text_file:
    text = text_file.read().lower()
    text = re.sub('[^0-9a-zA-Z\s:]+', '', text)
    tokens=nltk.word_tokenize(str(text))
    tokens = [w for w in tokens if not w in stopset]

depParser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

dependencyTree = [list(parse.triples()) for parse in depParser.raw_parse(text)]

topTerm = {}

for item in dependencyTree[0]:
    if (item[1] == 'amod'):
        if item not in topTerm:
            topTerm[item] = 1
        else:
            topTerm[item] = topTerm[item] + 1

print topTerm

