# encoding=utf8  
import os
import random
import requests
import json
from spacy.en import English
from nltk.classify import NaiveBayesClassifier
from flask import Flask, request, session, redirect, url_for, render_template

from TopReviewGenerator import TopReviewGenerator 

app = Flask(__name__)
nlp = English() 

source = open('data/trainData', 'rb').read()
trainData = eval(source)
classifier = NaiveBayesClassifier.train(trainData)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', search=True)
    else:
        return get_result()

def get_result():
    keyword = request.form.get('keyword', None)
    #movie = wikipedia.page(keyword + ' film')
    #moviePlot = movie.content.split("== Plot ==")[0]

    film_info = requests.get("http://www.omdbapi.com?t=" + keyword + "&y=&plot=short&r=json")
    info = film_info.json()

    review = TopReviewGenerator(keyword, nlp, classifier)

    highlights = review.getHighlight()
    highlightedReview = review.getReviewsWithHighlights(highlights)
    positiveReview = review.getPositiveReviewsCount()
    negativeReview = review.getNegativeReviewsCount()
    timeElapsed = review.getTimeElapsed()

    return render_template('index.html', key=keyword, movieInfo = info, result=highlights, reviewPerHighlight=highlightedReview, posCount=positiveReview, negCount=negativeReview, time=timeElapsed)