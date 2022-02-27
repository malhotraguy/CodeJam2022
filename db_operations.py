__author__ = "Rahul Malhotra"

from datetime import datetime, date
from pprint import pprint

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

from email_operations import send_email_alert
from sms_operations import send_sms_alert

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
usrn = os.environ.get("username")
passw = os.environ.get("password")
client = MongoClient(
    f"mongodb+srv://{usrn}:{passw}@snowclearancebuddy.7tjmg.mongodb.net/?retryWrites=true&w=majority")
snow_buddy_db = client.SnowBuddy


def check_db_availability(mongo_client: MongoClient) -> None:
    """

    :param mongo_client: Pymongo Client
    :return:
    """
    try:
        # The ping command is cheap and does not require auth.
        mongo_client.admin.command('ping')
    except ConnectionFailure:
        print("Server not available")


check_db_availability(mongo_client=client)


def find_number_complaints(address, threshold, complaint_type) -> int:
    """

    :param address:
    :param threshold:
    :param complaint_type:
    :return:
    """
    if complaint_type:
        complaints = snow_buddy_db.complaints.find({"address": address, "complaint_type": complaint_type})
    else:
        complaints = snow_buddy_db.complaints.find({"address": address})
    number_of_complaints = len(list(complaints))
    return number_of_complaints


def create_complaint(name: str, address: str, complaint_type: str, threshold: int = 5) -> dict:
    """

    :param name:
    :param address:
    :param complaint_type:
    :param threshold:
    :return:
    """
    snow_buddy_db.complaints.insert_one({"name": name, "address": address, "complaint_type": complaint_type})
    total_complaints = find_number_complaints(address=address, complaint_type=complaint_type, threshold=threshold)
    return {"Total no. of complaints registered": total_complaints}


def create_alert_subscription(person_name: str, address: str, mobile_number: str, email_id: str, sms_alert: bool,
                              email_alert: bool, app_alert: bool) -> None:
    """

    :param person_name:
    :param address:
    :param mobile_number:
    :param email_id:
    :param sms_alert:
    :param email_alert:
    :param app_alert:
    :return:
    """
    snow_buddy_db.alerts.update_one({"person_name": person_name, "address": address}, {
        "$set": {"mobile_number": mobile_number, "email_id": email_id, "sms_alert": sms_alert,
                 "email_alert": email_alert, "app_alert": app_alert}}, upsert=True)


def send_alert(address: str, message: str) -> str:
    """

    :param address:
    :param message:
    :return:
    """
    alert_emails = snow_buddy_db.alerts.find({"address": address, "email_alert": True}, {"_id": 0, "email_id": 1})
    alert_mobiles = snow_buddy_db.alerts.find({"address": address, "sms_alert": True}, {"_id": 0, "mobile_number": 1})
    alert_emails = [email.get("email_id") for email in alert_emails if email.get("email_id") is not None]
    alert_mobiles = [mobile.get("mobile_number") for mobile in alert_mobiles if mobile.get("mobile_number") is not None]
    for email in alert_emails:
        send_email_alert(alert_msg=message, receiver_email=email)
    for mobile in alert_mobiles:
        send_sms_alert(alert_msg=message, receiver_mobile=mobile)

    success_message = f"Alerted Mobiles:{alert_mobiles} \nAlerted Emails:{alert_emails}"
    pprint(success_message)
    return success_message


def set_approximation_data(address: str, approximation_in_mins: str) -> None:
    snow_buddy_db.streets.update_one({"address": address}, {
        "$set": {"clearing_status": "In Progress"}})
    todays_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    todays_doc = snow_buddy_db.cleaning_history.find_one(
        {"address": address, "apprx_alert_datetime": {"$gte": todays_date}})
    if todays_doc:
        snow_buddy_db.cleaning_history.update_one({"address": address}, {
            "$set": {"apprx_alert_datetime": datetime.utcnow(),
                     "approx_in_mins": approximation_in_mins}})
    else:
        snow_buddy_db.cleaning_history.insert_one(
            {"address": address, "apprx_alert_datetime": datetime.utcnow(),
             "approx_in_mins": approximation_in_mins})

