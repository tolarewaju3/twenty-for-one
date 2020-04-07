from google.cloud import datastore
import requests
import os

datastore_client = datastore.Client()

kind = 'NearbyZipCode'

ENDPOINT = "https://www.zipcodeapi.com/rest"

API_KEY = os.environ.get('ZIP_API_KEY', '')

MILE_RADIUS = "5"

def getNearbyZipCodes(zip):
	nearby_zip_codes = getNearbyZipCodesFromDatabase(zip)

	if len(nearby_zip_codes) == 0:
		print('No zip codes found. Fetching from API..')
		saveNearbyZipCodesFromAPI(zip)
	else: 
		print("Zip Codes Found in DB")
		return nearby_zip_codes


def getNearbyZipCodesFromDatabase(zip):
	zip_key = datastore_client.key(kind, zip)
	zip = datastore_client.get(zip_key)

	if zip is None:
		return []
	else: 
		return zip["nearby_zip_codes"]

def saveNearbyZipCodesFromAPI(zip):
	zip_api_url = getZipCodeURL(zip)

	r = requests.get(url = zip_api_url) 
	data = r.json()

	if r.status_code == 200:
		nearby_zip_codes = data["zip_codes"]
		if len(nearby_zip_codes) > 0:
			saveNearbyZipCodesToDB(zip, nearby_zip_codes)
	else:
		return 'Failure on web request'

def saveNearbyZipCodesToDB(zip, nearby_zip_codes):
	nearby_zip_objects = []

	for x in nearby_zip_codes:
		zip_key = datastore_client.key(kind, x)
		nearbyZip = datastore.Entity(key=zip_key)
		nearbyZip['nearby_zip_codes'] = nearby_zip_codes
		nearby_zip_objects.append(nearbyZip)

	datastore_client.put_multi(nearby_zip_objects)


def getZipCodeURL(zip):
	RESOURCE = "radius.json/%s/%s/miles?minimal" % (zip, MILE_RADIUS)
	URL = "%s/%s/%s" % (ENDPOINT, API_KEY, RESOURCE)

	return URL