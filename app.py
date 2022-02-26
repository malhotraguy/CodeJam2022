# Coded in python 3.8
__author__ = "Rahul Malhotra"

from pprint import pprint

from flask import Flask, jsonify

from db_operations import client

app = Flask(__name__)


@app.route('/')
def index():
    return 'Use /all_launches_timeline'


@app.route('/sample_launch/')
def sample():
    db = client.Test
    result = db.Creator.find({"Creator": "Rahul Malhotra"})
    result = str(list(result))
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
