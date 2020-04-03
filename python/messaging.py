from twilio.rest import Client
import os

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
