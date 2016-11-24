# encoding=utf8  
import nltk
import operator
import spacy
import sys
from spacy.en import English
from spacy.symbols import *
from MovieCriticSite import MovieCriticSite
from datetime import datetime
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from SentimentAnalyzer import SentimentAnalyzer

class TopReviewGenerator:

    def __init__(self, film):
        print(film)
        tick = datetime.now()
        self.nlp = English()

        self.film = film        
        self.reviews = self.scrapMovieReview(self.film, 1)

        sa = SentimentAnalyzer()
        self.sentiment = sa.classifyReviews(self.reviews)

        tock = datetime.now()   
        self.time = tock - tick

    def getTimeElapsed(self):
        return self.time

    def getAllReviews(self):
        return self.reviews

    def getPositiveReviewsCount(self):
        return len(self.sentiment["pos"])

    def getNegativeReviewsCount(self):
        return len(self.sentiment["neg"])

    def getPositiveReviews(self):
        return len(self.sentiment["pos"])

    def getHighlight(self):
        terms = {}
        for doc in self.reviews:
            for possible_adjective in self.nlp(str(doc, 'utf-8')):
                if (possible_adjective.dep == amod) and possible_adjective.head.pos == NOUN:
                    termFrase = possible_adjective.orth_ + ' ' + possible_adjective.head.orth_

                    if possible_adjective.head.head.pos == NOUN and possible_adjective.head.orth_ != possible_adjective.head.head.orth_:
                        termFrase += ' ' + possible_adjective.head.head.orth_

                    blob = TextBlob(termFrase)
                    if (blob.sentences[0].sentiment.polarity > 0.15 or blob.sentences[0].sentiment.polarity < -0.15):
                        terms[termFrase] = terms.get(termFrase, 0) + 1

        sorted_term = sorted(terms.items(), key=operator.itemgetter(1), reverse=True)
        top_term = sorted_term[:10]
        return top_term

    def scrapMovieReview(self, title, totalpage):
        rt = MovieCriticSite("Rotten Tomatoes")
        rt.setCritics("https://www.rottentomatoes.com/m/$film$/reviews/?page=$page$", "//div[@class=\"the_review\"]/text()")
        rt.setAudiences("https://www.rottentomatoes.com/m/$film$/reviews/?type=user&page=$page$", '//div[@class="user_review"]/text()[last()]')
        rt.setSearch("https://www.rottentomatoes.com/search/?search=$film$", "substring(//section[@id=\"SummaryResults\"]//ul/li//div[@class=\"poster\"]/a/@href, 4)")

        mc = MovieCriticSite("Metacritics")
        mc.setCritics("http://www.metacritic.com/movie/$film$/critic-reviews?page=$page$", "//div[@class=\"summary\"]/a[@class=\"no_hover\"]/text()")
        mc.setAudiences("http://www.metacritic.com/movie/$film$/user-reviews?page=$page$", "//div[@class=\"review_body\"]/span/span[@class=\"blurb blurb_expanded\"]/text()|//div[@class=\"review_body\"]/span/text()")
        mc.setSearch("http://www.metacritic.com/search/all/$film$/results", "substring(//li[@class=\"result first_result\"]//a/@href, 8)")

        imdb = MovieCriticSite("IMDB")
        #IMDB ga punya page khusus critics :(
        imdb.setAudiences("http://www.imdb.com/title/$film$/reviews?start=$page$", "//div[@id=\"tn15content\"]//div/h2/text()|//div[@class=\"review_body\"]/span/text()")
        imdb.setSearch("http://www.imdb.com/find?ref_=nv_sr_fn&q=$film$&s=all", "substring((//table[@class=\"findList\"])[1]/tr[@class=\"findResult odd\"][1]/td[@class=\"primary_photo\"]/a/@href, 8, 9)")

        reviews = [];
        for i in range(0,totalpage):
            for line in imdb.getReview(title, i*10, 'audiences'):
                if (self.is_ascii(line.encode('utf-8'))):
                    reviews.append(line.encode("utf-8").strip())
            for line in rt.getReview(title, i, 'audiences'):
                if (self.is_ascii(line.encode('utf-8'))):
                    reviews.append(line.encode("utf-8").strip())
            for line in mc.getReview(title, i, 'audiences'):
                if (self.is_ascii(line.encode('utf-8'))):
                    reviews.append(line.encode("utf-8").strip())
            for line in rt.getReview(title, i, 'critics'):
                if (self.is_ascii(line.encode('utf-8'))):
                    reviews.append(line.encode("utf-8").strip())
        for line in mc.getReview(title, 0, 'critics'):
            if (self.is_ascii(line.encode('utf-8'))):
                reviews.append(line.encode("utf-8").strip())
        return reviews

    def is_ascii(self, text):
        return all(c < 128 for c in text)

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def getReviewsWithHighlights(self, highlights):
        keys = []
        for highlight in highlights:
            keys.append(highlight[0])

        reviewsWithHighlights = {key: [] for key in keys}
        for review in self.reviews:
            for highlight in highlights:
                tmp = highlight[0].split(" ")
                if (tmp[0].encode('utf-8') in review and tmp[1].encode('utf-8') in review):
                    reviewsWithHighlights[highlight[0]].append(review)
        return reviewsWithHighlights
