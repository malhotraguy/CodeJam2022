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
db = client.Test
resp = db.Creator.find({"Creator": "Rahul Malhotra"})
pprint(list(resp))
