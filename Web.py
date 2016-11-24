# encoding=utf8  
import os
import random
from flask import Flask, request, session, redirect, url_for, render_template

from TopReviewGenerator import TopReviewGenerator 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', search=True)
    else:
        return get_result()

def get_result():
    keyword = request.form.get('keyword', None)

    review = TopReviewGenerator(keyword)

    highlights = review.getHighlight()
    highlightedReview = review.getReviewsWithHighlights(highlights)
    positiveReview = review.getPositiveReviewsCount()
    negativeReview = review.getNegativeReviewsCount()
    timeElapsed = review.getTimeElapsed()

    return render_template('index.html', key=keyword, result=highlights, reviewPerHighlight=highlightedReview, posCount=positiveReview, negCount=negativeReview, time=timeElapsed)