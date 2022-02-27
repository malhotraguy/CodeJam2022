__author__ = "Rahul Malhotra"

from pprint import pprint

import googlemaps
from flask import jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
usrn = os.environ.get("username")
passw = os.environ.get("password")
key = os.environ.get("key")
client = MongoClient(
    f"mongodb+srv://{usrn}:{passw}@snowclearancebuddy.7tjmg.mongodb.net/?retryWrites=true&w=majority")
snow_buddy_db = client.SnowBuddy

gmaps = googlemaps.Client(key=key)

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


def add_street(address, longitude, latitude, date_of_clearing, clearing_status):
    snow_buddy_db.streets.insert_one({"address":address, "longitude":longitude, "latitude":latitude, "date_of_clearing":date_of_clearing, "clearing_status":clearing_status})
    return {"Added address": ""}

def get_new_route():
    streets = snow_buddy_db.streets.find({"clearing_status": "False"})
    streets = list(streets)

    street_locations = []

    for street in streets:
        street_locations.append(street["longitude"] + " " + street["latitude"])

    result = gmaps.directions(street_locations[0], street_locations[0], mode="driving", waypoints=street_locations[1:])

    steps = ""

    steps = []

    for i, leg in enumerate(result[0]["legs"]):
        steps = steps + "Stop: " + str(i) + " " + str(leg["start_location"])\
                +" to " + " " + str(leg["end_location"])\
                + " distance: " + str(leg["distance"]["value"])\
                + " traveling Time: " +  str(leg["duration"]["value"]) + \
                "\n"

    print(steps)


    return steps

