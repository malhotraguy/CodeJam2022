# Coded in python 3.8
__author__ = "Rahul Malhotra"

import os
from datetime import datetime
from pprint import pprint

from flask import Flask, jsonify, request, render_template, url_for, flash, redirect

from db_operations import client, create_complaint, create_alert_subscription

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24).hex()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', utc_dt=datetime.utcnow())


@app.route('/creator/', methods=['GET', 'POST'])
def creator():
    db = client.Test
    result = db.Creator.find({"Creator": "Rahul Malhotra"})
    result = str(list(result))
    return jsonify(result)


@app.route('/complaint/', methods=['GET', 'POST'])
def register_complain():
    error = None
    if request.method == 'POST':
        person_name = request.form.get('name')
        address = request.form.get('address')
        complaint_type = request.form.get('complaint_type')
        if not person_name:
            flash('Name is required!')
            error = "Empty Name"
        elif not address:
            flash('Address is required!')
            error = "Empty Address"
        elif not complaint_type:
            flash('Complaint Type is required!')
            error = "Empty Complaint Type"
        else:
            result = create_complaint(person_name, address, complaint_type, threshold=5)
            error = result

    return render_template('complaints.html', error=error)


@app.route('/subscribe/', methods=['GET', 'POST'])
def alert_subscription():
    error = None
    if request.method == 'POST':
        person_name = request.args.get('name')
        address = request.args.get('address')
        mobile_number = request.args.get('mobile_number')
        email_id = request.args.get('email_id')
        app_alert = request.args.get('app_alert', "").lower() == "true"
        sms_alert = request.args.get('sms_alert', "").lower() == "true"
        email_alert = request.args.get('email_alert', "").lower() == "true"
        if not person_name:
            error = 'Name is required!'
            flash(error)
        elif not address:
            error = 'Address is required!'
            flash(error)
        elif not email_id and not mobile_number:
            error = "Either Email Id or Mobile is required !"
            flash(error)
        elif not sms_alert and not email_alert:
            error = "Either Email Alert or Mobile Alert is required !"
            flash(error)
        else:
            create_alert_subscription(person_name=person_name, address=address, mobile_number=mobile_number,
                                      email_id=email_id, sms_alert=sms_alert, email_alert=email_alert,
                                      app_alert=app_alert)
            error = "Success"

    return render_template('alert_subscription.html', error=error)


@app.route("/send_approximation/", methods=['GET', 'POST'])
def send_approximation_alerts():
    error = None
    if request.method == 'POST':
        address = request.args.get('address')
        approximation_in_mins = request.args.get('approximation_in_mins')
        if not address:
            error = 'Address is required!'
            flash(error)
        elif not approximation_in_mins:
            error = "Either Email Id or Mobile is required !"
            flash(error)
        else:
            # send_alert(address=address, approximation_in_mins=approximation_in_mins)
            error = "Success"

    return render_template('alert_subscription.html', error=error)


if __name__ == '__main__':
    app.run()
