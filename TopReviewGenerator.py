# encoding=utf8  
import sys
import operator
import nltk
import spacy
from spacy.en import English
from spacy.symbols import *
from MovieCriticSite import MovieCriticSite
from datetime import datetime
from textblob import TextBlob

reload(sys)  
sys.setdefaultencoding('utf8')

nlp = English()

def getHighlight(docs):
    terms = {}
    for doc in docs:
        for possible_adjective in nlp(unicode(doc)):
            if (possible_adjective.dep == amod) and possible_adjective.head.pos == NOUN:
                termFrase = possible_adjective.orth_ + ' ' + possible_adjective.head.orth_

                if possible_adjective.head.head.pos == NOUN and possible_adjective.head.orth_ != possible_adjective.head.head.orth_:
                    termFrase += ' ' + possible_adjective.head.head.orth_

                blob = TextBlob(termFrase)
                if (blob.sentences[0].sentiment.polarity > 0.05 or blob.sentences[0].sentiment.polarity < -0.05):
                    terms[termFrase] = terms.get(termFrase, 0) + 1

    sorted_term = sorted(terms.items(), key=operator.itemgetter(1), reverse=True)
    top_term = sorted_term[:10]
    return top_term

def scrapMovieReview(title, totalpage):
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
            reviews.append(line.encode("utf-8").strip())
        for line in rt.getReview(title, i, 'audiences'):
            reviews.append(line.encode("utf-8").strip())
        for line in mc.getReview(title, i, 'audiences'):
            reviews.append(line.encode("utf-8").strip())
        for line in rt.getReview(title, i, 'critics'):
            reviews.append(line.encode("utf-8").strip())
        for line in mc.getReview(title, i, 'critics'):
            reviews.append(line.encode("utf-8").strip())
    return reviews

def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def getReviewsWithHighlights(highlights, reviews):
    keys = []
    for highlight in highlights:
        keys.append(highlight[0])

    reviewsWithHighlights = {key: [] for key in keys}
    for review in reviews:
        for highlight in highlights:
            tmp = highlight[0].split(" ")
            if (is_ascii(str(review)) and not hasNumbers(str(review))):
                if (tmp[0] in review and tmp[1] in review):
                    reviewsWithHighlights[highlight[0]].append(review)
    return reviewsWithHighlights

def main():
    tick = datetime.now()
    title = "Fantastic Beasts"
    
    reviews = scrapMovieReview(title, 5)
    highlights = getHighlight(reviews)
    highlightReviews = getReviewsWithHighlights(highlights, reviews)


    for highlight in highlights:
        print "\n" + highlight[0] + "\n"
        for review in highlightReviews[highlight[0]]:
            print review

    # print(highlight)
    tock = datetime.now()   
    diff = tock - tick    # the result is a datetime.timedelta object
    print("Time Elapsed: " + str(diff.total_seconds()))

if __name__ == "__main__":
    main()