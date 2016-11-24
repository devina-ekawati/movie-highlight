import collections
import re
import itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from os import listdir
from os.path import isfile, join, dirname, abspath

class SentimentAnalyzer:

    def __init__(self):
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        self.negData = [(self.extractBigramFeature(movie_reviews.raw(fileids=[f])), 'neg') for f in negids]
        self.posData = [(self.extractBigramFeature(movie_reviews.raw(fileids=[f])), 'pos') for f in posids]

        self.trainData = self.negData + self.posData

    def extractBigramFeature(self, sentence, score_fn=BigramAssocMeasures.chi_sq, n=200):
        # sentence = re.sub('[^A-Za-z0-9]+', '', sentence)
        sentence = sentence.rstrip()
        sentence = sentence.lower()
        words = nltk.word_tokenize(str(sentence))
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(score_fn, n)

        return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

    def classifyReviews(self, reviews):
        results = {}
        classifier = NaiveBayesClassifier.train(self.trainData)

        for review in reviews:
            sentiment = classifier.classify(self.extractBigramFeature(review))
            results.setdefault(sentiment,[]).append(review)

        return results

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

