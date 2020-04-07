from google.cloud import datastore
import messaging
import zipcode

datastore_client = datastore.Client()

kind = 'Person'

def findMatch(person, zip, phone):
    nearbyPerson = getNearbyPerson(zip, person['age_group'])
    sendMatchMessages(person, nearbyPerson, phone)


def getNearbyPerson(zip, age_group):
	nearbyZipCodes = zipcode.getNearbyZipCodes(zip)

	if nearbyZipCodes is not None and len(nearbyZipCodes) > 0:
		query = datastore_client.query(kind=kind)
		query.add_filter('match', '=', None)

		if age_group == '1':
			query.add_filter('age_group', '=', '2')
		else:
			query.add_filter('age_group', '=', '1')

		results = list(query.fetch())
		nearbyPeople = list(filter(lambda person: person['zip'] in nearbyZipCodes, results))

		if len(nearbyPeople) > 0: 
			return nearbyPeople[0]

def sendMatchMessages(person, nearbyPerson, phone):
    if person['age_group'] == '1':
        messaging.sendMessage(phone, f"Ok. You'll get a text when someone around you can help. Stay safe!")
        
        if nearbyPerson is not None:
            messaging.sendMessage(nearbyPerson.key.name, f"We found someone in your area that needs help!\n\nType 'Yes' to confirm. If you're feeling sick, please type 'No'.")
            createMatch(nearbyPerson, person)

    elif nearbyPerson is not None:
        messaging.sendMessage(phone,f"We found someone in your area that needs help!\n\nType 'Yes' to confirm. If you're feeling sick, please type 'No'.")
        createMatch(nearbyPerson, person)
    else:
        messaging.sendMessage(phone,f"Ok. You'll get a text when someone around you needs help. Stay safe!")

def createMatch(nearbyPerson, person):
	nearbyPerson['match'] = person.key
	person['match'] = nearbyPerson.key
	datastore_client.put_multi([nearbyPerson, person])
