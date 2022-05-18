from flask import Flask, request, jsonify
from fuzzy import simulate
from operator import itemgetter
from random import choice

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/ticket", methods=['POST'])
def check_ticket_advise():
    content = request.json
    price, comfort, travelTime = itemgetter('price', 'comfort', 'travelTime')(content)
    return jsonify(simulate(price, comfort, travelTime))


@app.route("/sentiment", methods=['POST'])
def check_sentiment():
    content = request.json['text']
    print(content)
    return jsonify({ 'sentiment': choice(['positivo', 'negativo']) })


if __name__ == "__main__":
    app.run(host='0.0.0.0')
