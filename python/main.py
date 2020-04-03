from google.cloud import datastore
import messaging
import match

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
        person = datastore.Entity(key=person_key)
        person['confirmed'] = False
        messaging.sendMessage(phone, f'Welcome to Twenty for One! We help get free groceries (under $20) to older adults at high risk of COVID-19. One more death is too many. What is your name?')
    elif "name" not in person:
        person['name'] = param
        messaging.sendMessage(phone, f"Nice to meet you, " + param + "! " + "Type 1 if you're an older adult. Type 2 if you're a younger adult willing to help")

    elif "age_group" not in person:
        person['age_group'] = param
        messaging.sendMessage(phone, f"Great! What's your zip code?")

    elif "zip" not in person:
        person['zip'] = param

        nearbyPerson = match.getNearbyPerson(param, person['age_group'])
        sendMatchMessages(person, nearbyPerson, phone)

        person['confirmed'] = True
    elif "match" in person:
        if person['age_group'] == '2':
            if param.lower() == 'yes':
                sendConfirmation(person, phone)
 

    datastore_client.put(person)
    return message

def sendMatchMessages(person, nearbyPerson, phone):
    if person['age_group'] == '1':
        messaging.sendMessage(phone, f"Ok. You'll get a text when someone around you can help. Stay safe!")
        
        if nearbyPerson is not None:
            messaging.sendMessage(nearbyPerson.key.name, f"We found someone in your area that needs help! Type 'Yes' to confirm. Please don't confirm if you're feeling sick.")
            nearbyPerson['match'] = person.key
            datastore_client.put(nearbyPerson)

    elif nearbyPerson is not None:
        messaging.sendMessage(phone,f"We found someone in your area that needs help! Type 'Yes' to confirm. Please don't confirm if you're feeling sick.")
        person['match'] = nearbyPerson.key
    else:
        messaging.sendMessage(phone,f"Ok. You'll get a text when someone around you needs help. Stay safe!")

def sendConfirmation(person, phone):
    olderAdult = datastore_client.get(person['match'])
    olderAdult['match'] = person.key
    datastore_client.put(olderAdult)

    messaging.sendMessage(phone,f"Great! Thanks for helping out! We've let them you know can help. Contact " + olderAdult['name'] + " at " + olderAdult.key.name + "." + "\n Remember to wash your hands before delivery :)")

    messaging.sendMessage(olderAdult.key.name, f"We found someone in your area that can help! Their name is " + olderAdult['name'] + "When they contact you, send them your grocery list and address. Your first $20 will be delivered free. So put the most important items first :)")

