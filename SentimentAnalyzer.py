import collections
import re
import itertools
import threading
import json
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from os import listdir
from os.path import isfile, join, dirname, abspath
from datetime import datetime

class SentimentAnalyzer:

    def __init__(self):
        self.results = {}
        #source = open('data/trainData', 'rb').read()
        #self.trainData = eval(source)
        #self.classifier = NaiveBayesClassifier.train(self.trainData)

    def prepareBigramData(self):
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        tock = datetime.now()   
        print("Start collectin data at " + str(tock))

        negData = [(self.extractBigramFeature(movie_reviews.raw(fileids=[f])), 'neg') for f in negids]
        posData = [(self.extractBigramFeature(movie_reviews.raw(fileids=[f])), 'pos') for f in posids]

        tock = datetime.now()   
        print("All thread finished collectin data at " + str(tock))

        trainData = negData + posData

        #with open('data/trainData', 'wb') as dump:
        #    dump.write(json.dumps(trainData))
        
        with open('data/trainData', 'wb') as dump:
            dump.write(str(trainData))


    def getClassifyResults(self):
        return self.results

    def extractBigramFeature(self, sentence, score_fn=BigramAssocMeasures.chi_sq, n=200):
        # sentence = re.sub('[^A-Za-z0-9]+', '', sentence)
        sentence = sentence.rstrip()
        sentence = sentence.lower()
        words = nltk.word_tokenize(str(sentence))
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(score_fn, n)

        return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

    def classifyReviews(self, reviews):
        for review in reviews:
            sentiment = self.classifier.classify(self.extractBigramFeature(review))
            self.results.setdefault(sentiment,[]).append(review)

    def evaluate_classifier(self):
        negCutOff = len(self.negData)*3/4
        posCutOff = len(self.posData)*3/4
     
        trainData = self.negData[:negCutOff] + self.posData[:posCutOff]
        testData = self.negData[negCutOff:] + self.posData[posCutOff:]
     
        classifier = NaiveBayesClassifier.train(trainData)
        refsets = collections.defaultdict(set)
        testSets = collections.defaultdict(set)
     
        for i, (feats, label) in enumerate(testData):
                refsets[label].add(i)
                observed = classifier.classify(feats)
                testSets[observed].add(i)
     
        #print 'accuracy:', nltk.classify.util.accuracy(classifier, testData)


if __name__ == "__main__":
    reviews = []

    with open("test.txt") as f:
        reviews = f.readlines()

    sa = SentimentAnalyzer()
    # sa.evaluate_classifier()
    sa.classifyReviews(reviews)

