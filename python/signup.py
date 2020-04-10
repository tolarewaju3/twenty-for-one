from google.cloud import datastore
import messaging
import match
import re

datastore_client = datastore.Client()

kind = 'Person'

def createNewPerson(person_key, phone):
    person = datastore.Entity(key=person_key)
    person['match'] = None;
    messaging.sendMessage(phone, f"Welcome to Twenty for One! We deliver $20 of free groceries to people at high risk of COVID-19. We believe that even one more death is too many. Anyway, what's your first name?")
    datastore_client.put(person)

def saveName(person, param, phone):
    person['name'] = param
    messaging.sendMessage(phone, f"Nice to meet you, " + param + "! " + "\n\nType 1 if you're an older adult.\nType 2 if you're a younger adult willing to help")
    datastore_client.put(person)

def saveAge(person, param, phone):
    isValidGroup = re.search("^(1|2)$", param)

    if isValidGroup != None:
        person['age_group'] = param
        messaging.sendMessage(phone, f"Great! What's your zip code?")
        datastore_client.put(person)
    else:
        messaging.sendMessage(phone, f"Oops! \n\nPlease type 1 if you're an older adult.\nType 2 if you're a younger adult willing to help")

def saveZip(person, param, phone):
    isValidZip = re.search("^\d{5}$", param)
    if isValidZip != None:
        person['zip'] = param
        person['confirmed'] = True;
        datastore_client.put(person)
        match.findMatch(person, param, phone)
    else:
        messaging.sendMessage(phone, f"Oops! We need valid 5 digit zip code..")
