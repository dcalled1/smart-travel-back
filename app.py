from flask import Flask, request, jsonify
from fuzzy import simulate
from operator import itemgetter

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/ticket", methods=['POST'])
def check_ticket_advise():
    content = request.json
    price, comfort, travelTime = itemgetter('price', 'comfort', 'travelTime')(content)
    return jsonify(simulate(price, comfort, travelTime))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
