from google.cloud import datastore
import zipcode

datastore_client = datastore.Client()

kind = 'Person'


def getNearbyPerson(zip, age_group):
	nearbyZipCodes = zipcode.getNearbyZipCodes(zip)

	if nearbyZipCodes is not None and len(nearbyZipCodes) > 0:
		query = datastore_client.query(kind=kind)
		query.add_filter('confirmed', '=', True)

		if age_group == '1':
			query.add_filter('age_group', '=', '2')
		else:
			query.add_filter('age_group', '=', '1')

		results = list(query.fetch())
		nearbyPeople = list(filter(lambda person: person['zip'] in nearbyZipCodes, results))

		if len(nearbyPeople) > 0: 
			print(nearbyPeople[0])
			return nearbyPeople[0]
