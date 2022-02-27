__author__ = "Rahul Malhotra"

import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def send_sms_alert(alert_msg, receiver_mobile):
    try:
        message = client.messages.create(
            body=alert_msg,
            from_='+19084989182',
            to=receiver_mobile
        )

        print(message.sid)
    except Exception as e:
        print("Exception!!")
        print(e)


if __name__ == '__main__':
    send_sms_alert(alert_msg="SMS Alerts are working!!", receiver_mobile="+15148349361")
