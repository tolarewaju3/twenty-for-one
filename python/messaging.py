from google.cloud import datastore
from twilio.rest import Client
import datetime
import os

kind = 'Event'

datastore_client = datastore.Client()

def sendMessage(phone, message):
	account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
	auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')

	if account_sid is not '' and auth_token is not '':
		print("here")
		client = Client(account_sid, auth_token)

		message = client.messages \
			.create(body=message, from_='+15123127461',to=phone)
	else:
		print("No Twilio Credentials. Printing message for phone: " + phone + "\n")
		print(message)
		print("")

def saveActivity(message, type):
    event_key = datastore_client.key(kind)

    event = datastore.Entity(key=event_key)

    event['message'] = message;
    event['create_date'] = datetime.datetime.utcnow()
    event['type'] = type;

    datastore_client.put(event)