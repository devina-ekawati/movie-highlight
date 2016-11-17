import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

class SentimentAnalyzer:

    def __init__(self, feature):
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')

        self.negData = [(feature(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        self.posData = [(feature(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

        self.trainData = self.negData + self.posData
        self.testData = []



    def classify(self):
        classifier = NaiveBayesClassifier.train(self.trainData)

        for i, (feats, label) in enumerate(testfeats):
            print classifier.classify(feats)

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
     
        print 'accuracy:', nltk.classify.util.accuracy(classifier, testData)

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)

    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

sa = SentimentAnalyzer(bigram_word_feats)
sa.evaluate_classifier()

