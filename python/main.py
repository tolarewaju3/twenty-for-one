from google.cloud import datastore
import messaging
import match
import datetime

datastore_client = datastore.Client()

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
        createNewPerson(person_key, phone)
        
    elif "name" not in person:
        saveName(person, param, phone)

    elif "age_group" not in person:
        saveAge(person, param, phone);

    elif "zip" not in person:
        saveZip(person, param, phone)
    elif "match" in person and "delivery" not in person:
        if person['age_group'] == '2':
            if param.lower() == 'yes':
                olderAdult = datastore_client.get(person['match'])
                setUpDelivery(person, olderAdult, phone)
    elif "delivery" in person:
        confirmDelivery(person, param, phone)


    return message

def createNewPerson(person_key, phone):
    person = datastore.Entity(key=person_key)
    person['confirmed'] = False
    messaging.sendMessage(phone, f"Welcome to Twenty for One! We deliver $20 of free groceries to people at high risk of COVID-19. Because even one more death is too many. Anyway, what's your name?")
    datastore_client.put(person)

def saveName(person, param, phone):
    person['name'] = param
    messaging.sendMessage(phone, f"Nice to meet you, " + param + "! " + "Type 1 if you're an older adult. Type 2 if you're a younger adult willing to help")
    datastore_client.put(person)

def saveAge(person, param, phone):
    person['age_group'] = param
    messaging.sendMessage(phone, f"Great! What's your zip code?")
    datastore_client.put(person)

def saveZip(person, param, phone):
    person['zip'] = param

    nearbyPerson = match.getNearbyPerson(param, person['age_group'])
    sendMatchMessages(person, nearbyPerson, phone)

    person['confirmed'] = True
    datastore_client.put(person)


def sendMatchMessages(person, nearbyPerson, phone):
    if person['age_group'] == '1':
        messaging.sendMessage(phone, f"Ok. You'll get a text when someone around you can help. Stay safe!")
        
        if nearbyPerson is not None:
            messaging.sendMessage(nearbyPerson.key.name, f"We found someone in your area that needs help! Type 'Yes' to confirm. Please don't confirm if you're feeling sick.")
            nearbyPerson['match'] = person.key
            datastore_client.put(nearbyPerson)

    elif nearbyPerson is not None:
        messaging.sendMessage(phone,f"We found someone in your area that needs help! Type 'Yes' to confirm. If you're feeling sick, please type 'No'.")
        person['match'] = nearbyPerson.key
    else:
        messaging.sendMessage(phone,f"Ok. You'll get a text when someone around you needs help. Stay safe!")

def setUpDelivery(person, olderAdult, phone):
    olderAdult['match'] = person.key
                ## do we need this?

    delivery_key = datastore_client.key('Delivery', phone)
    delivery = datastore.Entity(key=delivery_key)
    delivery['create_date'] = datetime.datetime.utcnow()
    delivery['helper'] = person['name']
    delivery['needed_help'] = olderAdult['name']
    delivery['zip'] = olderAdult['zip']

    person['delivery'] = delivery.key

    datastore_client.put_multi([olderAdult, delivery, person])

    messaging.sendMessage(phone,f"Great! Contact " + olderAdult['name'] + " at " + olderAdult.key.name + "." + "\n1. Remember to wash your hands before delivery\n2. Text 'DONE' after you deliver so we can post about you\n3. Thanks again! ")

    messaging.sendMessage(olderAdult.key.name, f"We found someone near you that can help! Their name is " + person['name'] + ". " + "When they contact you, send your address and grocery list. We buy your first $20, so put the most important items first :)")

def confirmDelivery(person, param, phone):
    if person['age_group'] == '2':
        if param.lower() == 'done':
            delivery = datastore_client.get(person['delivery'])
            delivery['done_date'] = datetime.datetime.utcnow()

            datastore_client.put(delivery)

            messaging.sendMessage(phone, f"Sweet! Thanks for confirming delivery. We put your name up on the dashboard at twentyforone.com. You're awesome!")
