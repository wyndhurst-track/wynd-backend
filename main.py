from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

cows = [
    "moo 1",
    "moo 2",
    "moo 3",
    "moo 4",
    "moo 5",
    "moo 6",
    "moo 7",
    "moo 8",
    "moo 9"
]

@app.route("/cows")
def hello_world():
  return jsonify(cows)
