import nltk
import re
from nltk.parse.stanford import StanfordDependencyParser
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import operator
import os
from MovieCriticSite import MovieCriticSite

depParser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
listTopReviews = []
lines = []

def init():
    java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
    os.environ['JAVAHOME'] = java_path

def getTopTerm(path):
    topTerm = {}
    # for text in lines:
    #     sentences = sent_tokenize(text.strip())
    #     for sentence in sentences:
    #         dependencyTree = [list(parse.triples()) for parse in depParser.raw_parse(sentence)]
    #         for item in dependencyTree[0]:
    #             if (item[1] == 'amod'):
    #                 newitem = (item[0][0],item[2][0])
    #                 if newitem not in topTerm:
    #                     topTerm[newitem] = 1
    #                 else:
    #                     topTerm[newitem] = topTerm[newitem] + 1
    with open(path, 'r') as text_file:
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

    for term in topTerm:
        string = term[0][1] + " " + term[0][0]
        listTopReviews.append(string)

    return topTerm

def printReviewSequences(topTerm):
    seq = {key: [] for key in listTopReviews}

    for line in lines:
        for highlight in listTopReviews:
            tmp = highlight.split(" ")
            if (tmp[0] in line and tmp[1] in line):
                seq[highlight].append(line)

    with open("result.txt", "w") as text_file:
        for highlight in listTopReviews:
            text_file.write(highlight)
        for review in seq[highlight]:
            text_file.write(review)
    text_file.close()

def scrapMovieReview(title):
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

    print('Reviews: ', imdb.getReview(title, 0, 'audiences'))


def main():
    init()
    path = "rottentomatoes.txt"
    title = "Doctor Stranger"
    topTerm = getTopTerm(path)
    print topTerm
    printReviewSequences(topTerm)
    # scrapMovieReview(title)

if __name__ == "__main__":
    main()