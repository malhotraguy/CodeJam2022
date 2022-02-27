__author__ = "Rahul Malhotra"

from pprint import pprint

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
usrn = os.environ.get("username")
passw = os.environ.get("password")
client = MongoClient(
    f"mongodb+srv://{usrn}:{passw}@snowclearancebuddy.7tjmg.mongodb.net/?retryWrites=true&w=majority")
snow_buddy_db = client.SnowBuddy


# db = client.Test
# resp = db.Creator.find({"Creator": "Rahul Malhotra"})
# pprint(list(resp))

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


def find_number_complaints(address, threshold, complaint_type):
    if complaint_type:
        compliants = snow_buddy_db.complaints.find({"address": address, "complaint_type": complaint_type})
    else:
        compliants = snow_buddy_db.complaints.find({"address": address})
    number_of_complaints = len(list(compliants))
    return number_of_complaints


def create_complaint(name, address, complaint_type, threshold=5):
    snow_buddy_db.complaints.insert_one({"name": name, "address": address, "complaint_type": complaint_type})
    total_complaints = find_number_complaints(address=address, complaint_type=complaint_type, threshold=threshold)
    return {"Total no. of complaints registered": total_complaints}


def create_alert_subscription(person_name: str, address: str, mobile_number: str, email_id: str, sms_alert: bool,
                              email_alert: bool, app_alert: bool):
    snow_buddy_db.alerts.update_one({"person_name": person_name, "address": address}, {
        "$set": {"mobile_number": mobile_number, "email_id": email_id, "sms_alert": sms_alert,
                 "email_alert": email_alert, "app_alert": app_alert}}, upsert=True)
