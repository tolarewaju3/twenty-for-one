from google.cloud import datastore
import messaging
import signup
import match
import delivery

datastore_client = datastore.Client()

kind = 'Person'

def start(request):
    request_json = request.get_json()
    
    if request.args and 'From' in request.args:
        phone = request.args.get('From')
    
    if request.args and 'Body' in request.args:
        param = request.args.get('Body')
    
    return twentyForOne(phone, param)
   

def twentyForOne(phone, param):
    person_key = datastore_client.key(kind, phone)
    person = datastore_client.get(person_key)

    if person is None:
        signup.createNewPerson(person_key, phone)
        
    elif "name" not in person:
        signup.saveName(person, param, phone)

    elif "age_group" not in person:
        signup.saveAge(person, param, phone);

    elif "zip" not in person:
        signup.saveZip(person, param, phone);
        match.findMatch(person, param, phone)
    elif "match" in person and "delivery" not in person:
        if person['age_group'] == '2' and param.lower() == 'yes':
            delivery.setUpDelivery(person, phone)
    elif "delivery" in person:
        delivery.confirmDelivery(person, param, phone)

    return "OK"


