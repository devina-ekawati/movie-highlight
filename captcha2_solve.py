import requests
import re

sess = requests.Session()
url = 'http://localhost:5002/'
r = sess.get(url)
n = 0
while 1:
    if "HMIF{" in r.text:
        print(r.text)
        break
    elif "Wrong" in r.text:
        print("Wrong???")
        break
    captcha = re.findall(r"\<code\>(.*)\</code\>", r.text)[0]
    captcha = " " + captcha
    for f in [" b", " o", " x"]:
        captcha = captcha.replace(f, " 0" + f[1])
    solution = str(eval(captcha))
    data = {"captcha": solution}
    r = sess.post(url, data=data)
    n += 1
    if n == 199:
        print(r.text)
    print(n)