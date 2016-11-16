import os
import random
from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)

N_CAPTCHA = 200
FLAG = "HMIF{this_kind_of_task_is_boring_but_necessary}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        captcha = generate_captcha(0)
        session['level'] = 0
        session['captcha'] = captcha
        return render_template('index.html', captcha=captcha['captcha'])
    else:
        return handle_captcha()

def handle_captcha():
    solution = request.form.get('captcha', None)
    captcha = session.get('captcha', None)
    level = session.get('level', None)
    if solution is None or captcha is None or level is None:
        return redirect(url_for('index'))
    real_solution = captcha.get('solution', None)
    if real_solution == solution:
        message = "Correct! How about this?"
        error = None
        level += 1
    else:
        message = "Wrong! You're not robot!"
        error = True
        level = 0
    captcha = generate_captcha(level)
    session['captcha'] = captcha
    session['level'] = level
    if level >= N_CAPTCHA:
        message = "Congrats! The flag is: {}".format(FLAG)
        return render_template('index.html', message=message)
    else:
        return render_template('index.html', message=message, captcha=captcha['captcha'], error=error)

def generate_captcha(level):
    assert(level >= 0)
    number_set = [i for i in range(1, 21)]
    operator_set = ["+", "-", "*"]
    numbers = [random.choice(number_set) for _ in range(level+2)]
    operators = [random.choice(operator_set) for _ in range(level+1)]
    formats = [bin, hex, oct, int]
    captcha = []
    for i in range(level+2):
        op =  random.choice(formats)
        captcha.append(str(op(numbers[i])))
        if i < level+1:
            captcha.append(operators[i])
    solution = str(eval(" ".join(captcha)))
    for i in range(len(captcha)):
        if i & 1: continue
        for f in ["0b", "0x", "0o"]:
            if captcha[i].startswith(f):
                captcha[i] = captcha[i][1:]
                break
    return {"captcha": " ".join(captcha), "solution": solution}
