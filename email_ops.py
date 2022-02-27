__author__ = "Rahul Malhotra"

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()  # use dotenv to hide sensitive credential as environment variables
password = os.environ.get("SENDGRID_API_KEY")


def send_email_alert(alert_msg, receiver_email):
    message = Mail(
        from_email='matterisfull@gmail.com',
        to_emails=receiver_email,
        subject='Snow Clearance Buddy Alert',
        html_content=f'<strong>{alert_msg}</strong>')
    try:
        sg_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg_client.send(message)

    except Exception as e:
        print("Exception!!")
        print(e.message)


if __name__ == '__main__':
    send_email_alert(alert_msg="Email Alerts are working!!", receiver_email="electronicsgrad@gmail.com")