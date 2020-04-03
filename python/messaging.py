from twilio.rest import Client
import os

def sendMessage(phone, message):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=message,
            from_='+15123127461',
            to=phone
        )