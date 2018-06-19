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
