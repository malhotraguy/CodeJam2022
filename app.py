# Coded in python 3.8
__author__ = "Rahul Malhotra"

import os
from datetime import datetime

from flask import Flask, jsonify, request, render_template, url_for, flash, redirect

from db_operations import client, create_complaint, create_alert_subscription, send_alert

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
    """

    :return:
    """
    error = None
    if request.method == 'POST':
        person_name = request.form.get('name')
        address = request.form.get('address')
        complaint_type = request.form.get('complaint_type')
        if not person_name:
            error = "Name is required!"
        elif not address:
            error = "Address is required!"
        elif not complaint_type:
            error = "Complaint Type is required!"
        else:
            result = create_complaint(person_name, address, complaint_type, threshold=5)
            error = result
        flash(message=error)

    return render_template('complaints.html', error=error)


@app.route('/subscribe/', methods=['GET', 'POST'])
def alert_subscription():
    """

    :return:
    """
    error = None
    if request.method == 'POST':
        person_name = request.form.get('name')
        address = request.form.get('address')
        mobile_number = request.form.get('mobile_number')
        email_id = request.form.get('email_id')
        app_alert = request.form.get('app_alert', "").lower() == "true"
        sms_alert = request.form.get('sms_alert', "").lower() == "true"
        email_alert = request.form.get('email_alert', "").lower() == "true"
        if not person_name:
            error = 'Name is required!'
        elif not address:
            error = 'Address is required!'
        elif not email_id and not mobile_number:
            error = "Either Email Id or Mobile is required !"
        elif not sms_alert and not email_alert:
            error = "Either Email Alert or Mobile Alert is required !"
        else:
            create_alert_subscription(person_name=person_name, address=address, mobile_number=mobile_number,
                                      email_id=email_id, sms_alert=sms_alert, email_alert=email_alert,
                                      app_alert=app_alert)
            error = "Success"
        flash(error)

    return render_template('alert_subscription.html', error=error)


@app.route("/send_approximation/", methods=['GET', 'POST'])
def send_approximation_alerts():
    """

    :return:
    """
    error = None
    if request.method == 'POST':
        address = request.form.get('address')
        approximation_in_mins = request.form.get('approximation_in_mins')
        if not address:
            error = 'Address is required!'
        elif not approximation_in_mins:
            error = "Either Email Id or Mobile is required !"
        else:
            message = f"Snow removing vehicle will be on street in next: {approximation_in_mins} mins (approx.)"
            error = send_alert(address=address, message=message)
        flash(error)

    return render_template('approximation.html', error=error)


if __name__ == '__main__':
    app.run()
