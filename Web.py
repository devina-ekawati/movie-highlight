import os
import random
from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', search=True)
    else:
        return handle_captcha()

def get_result():
    keyword = request.form.get('keyword', None)
    return render_template('index.html', result=result)