import requests
import config
import json

def getNearbyPlaces(food_type, coords, radius=5000):
	print("GETTING NEARBY PLACES")

	lat, long = coords
	type='restaurant'

	url = ('{url}?'
	'location={lat},{long}'
	'&radius={radius}'
	'&type={type}'
	'&keyword={food_type}'
	'&key={key}'
	.format(url= config.PLACE_URL, lat=lat, long=long, radius=radius, type=type, food_type=food_type, key=config.MAPS_API_KEY))

	print("The url is: ", url)

	res = requests.get(url)
	res = res.json()

	results = res['results']

	topRestaurantName = None

	if len(results) > 0:
		topRestaurantName = results[0]['name']

	return topRestaurantName

def getLatLong(address):

	print("getting coords")
	print(address)

	url = ('{url}?'
	'address={address}'
	'&key={key}'
	.format(url= config.LOCATION_URL, address=address, key=config.MAPS_API_KEY))

	res = requests.get(url)
	res = res.json()
	results = res['results']

	if len(results) > 0:
		lat = results[0]['geometry']['location']['lat']
		long = results[0]['geometry']['location']['lng']
		return (lat, long)
	else:
		return None
