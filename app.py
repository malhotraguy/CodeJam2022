# Coded in python 3.8
__author__ = "Rahul Malhotra"

import os
from datetime import datetime
from string import Template

from flask import Flask, jsonify, request, render_template, url_for, flash, redirect

from db_operations import client, create_complaint, create_alert_subscription, send_alert, set_approximation_data

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

    return render_template('complaints.html')


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

    return render_template('alert_subscription.html')


@app.route("/send_approximation/", methods=['GET', 'POST'])
def send_approximation_alerts(redirect_to_finish=False):
    """

    :param redirect_to_finish:
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
            set_approximation_data(address, approximation_in_mins)
            redirect_to_finish = True
        flash(error)
        if redirect_to_finish:
            now_time = datetime.utcnow()
            return redirect(url_for("success", data=request.form, start_time=now_time), code=307)

    return render_template('approximation.html')


@app.route("/success/", methods=['GET', 'POST'])
def success():
    address = request.form.get('address')
    approximation_in_mins = request.form.get('approximation_in_mins')
    start_time_str = request.args.get("start_time")
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
    STATIC_MAP_TEMPLATE = Template("""
    <img src="https://maps.googleapis.com/maps/api/staticmap?size=700x300&markers=${place_name}" alt="map of ${place_name}">
    """)

    STREET_VIEW_TEMPLATE = Template("""
    <img src="https://maps.googleapis.com/maps/api/streetview?size=700x300&location=${place_name}" alt="street view of ${place_name}">
    """)
    return (f"""<h1>Started at: {start_time} Street: {address}, approx: {approximation_in_mins}</h1>"""+
            STATIC_MAP_TEMPLATE.substitute(place_name="Montreal") +
            STREET_VIEW_TEMPLATE.substitute(place_name="Montreal")
    )


if __name__ == '__main__':
    app.run()
