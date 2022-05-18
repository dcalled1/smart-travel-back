from flask import Flask, request, jsonify
from fuzzy import simulate, load_fuzzy_controller
from sentiment import classify, load_model
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
    sentiment = classify(content)
    return jsonify({ 'sentiment': sentiment })


if __name__ == "__main__":
    print('Loading fuzzy controller')
    load_fuzzy_controller()
    print('Loading sentiment analisys model')
    load_model()
    app.run(host='0.0.0.0')
