from flask import Flask, render_template, request, redirect
from texttostreet import get_streetmix_json
import urllib.parse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/querytext', methods=['GET', 'POST'])
def querytext():
    user_query = request.form['query']
    if user_query:
        streetmix_json = get_streetmix_json(user_query)
        #return render_template('localhost:7001/index-bot.html', street_json=streetmix_json)
        localhost_url = 'http://localhost:7001/index-bot.html'
        street_url = "{localhost}#streetmix-json:{streetmix_json}".format(
            localhost=localhost_url,
            streetmix_json=urllib.parse.quote(streetmix_json)
        )
        return redirect(street_url)

@app.route('/json_street', methods=['GET', 'POST'])
def json_street():
    user_query = request.form['query']
    if user_query:
        streetmix_json = get_streetmix_json(user_query)
        return streetmix_json


if __name__ == "__main__":
    app.run()