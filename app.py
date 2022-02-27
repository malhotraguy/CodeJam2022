# Coded in python 3.8
__author__ = "Rahul Malhotra"

from pprint import pprint

from flask import Flask, jsonify, request

from db_operations import client, create_complaint

app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to Snow Clearance Buddy App!!'


@app.route('/creator/')
def creator():
    db = client.Test
    result = db.Creator.find({"Creator": "Rahul Malhotra"})
    result = str(list(result))
    return jsonify(result)


@app.route('/complaint/', methods=["GET"])
def register_complain():
    person_name = request.args.get('name')
    address = request.args.get('address')
    complaint_type = request.args.get('complaint_type')
    result = create_complaint(person_name, address, complaint_type, threshold=5)
    return result


if __name__ == '__main__':
    app.run()
