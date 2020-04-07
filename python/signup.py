from google.cloud import datastore
import messaging

datastore_client = datastore.Client()

kind = 'Person'

def createNewPerson(person_key, phone):
    person = datastore.Entity(key=person_key)
    person['confirmed'] = False
    person['match'] = None;
    messaging.sendMessage(phone, f"Welcome to Twenty for One! We deliver $20 of free groceries to people at high risk of COVID-19. We believe that even one more death is too many. Anyway, what's your name?")
    datastore_client.put(person)

def saveName(person, param, phone):
    person['name'] = param
    messaging.sendMessage(phone, f"Nice to meet you, " + param + "! " + "\n\nType 1 if you're an older adult.\nType 2 if you're a younger adult willing to help")
    datastore_client.put(person)

def saveAge(person, param, phone):
    person['age_group'] = param
    messaging.sendMessage(phone, f"Great! What's your zip code?")
    datastore_client.put(person)

def saveZip(person, param, phone):
    person['zip'] = param
    datastore_client.put(person)