# Coded in python 3.8
__author__ = "Rahul Malhotra"

from pprint import pprint

import googlemaps

from flask import Flask, jsonify, request

from db_operations import client, create_complaint, add_street, get_new_route

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

#This endpoint can be used to quickly add streets in the database
@app.route('/add/', methods=["GET"])
def add_new_street():
    address = request.args.get('address')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    date_of_clearing = request.args.get('date_of_clearing')
    clearing_status = request.args.get('clearing_status')
    return add_street(address, longitude, latitude, date_of_clearing, clearing_status)


#This endpoint returns the computed route
@app.route('/compute/')
def showStreets():
    return get_new_route()


if __name__ == '__main__':
    app.run()
