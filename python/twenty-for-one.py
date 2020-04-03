from google.cloud import datastore
from twilio.rest import Client
import os

# Instantiates a client
datastore_client = datastore.Client()

# The kind for the new entity
kind = 'Person'

def findNearbyPeople(request):
    phone = '000-000-0000'
    param = 'hi'

    request_json = request.get_json()
    
    if request.args and 'From' in request.args:
        phone = request.args.get('From')
    
    if request.args and 'Body' in request.args:
        param = request.args.get('Body')
    
    return savePerson(phone, param)
   

def savePerson(phone, param):
    message = ''
    person_key = datastore_client.key(kind, phone)

    person = datastore_client.get(person_key)

    if person is None:
        person = datastore.Entity(key=person_key)
        message = f'Welcome to Twenty for One! We help get free groceries (under $20) to older adults at high risk of COVID-19. One more death is too many. What is your name?'
    elif "name" not in person:
        person['name'] = param
        message = f"Nice to meet you, " + param + "! " + "Type 1 if you're an older adult. Type 2 if you're a younger adult willing to help"
    elif "age_group" not in person:
        person['age_group'] = param
        message = f"Great! What's your zip code?"
    elif "zip" not in person:
        person['zip'] = param

        if person['age_group'] == '1':
            message = f"Ok. You'll get a text when someone around you can help. Stay safe!"
        else:
            message = f"Ok. You'll get a text when someone around you needs help. Stay safe!"
    
    datastore_client.put(person)
    sendMessage(phone, message)
    return message

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
