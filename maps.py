import requests
import secrets
import json
from pprint import pprint

params = {"key": secrets.GOOGLE_API_KEY, 
          "address": "Bend, OR"}

# response = requests.get('https://maps.googleapis.com/maps/api/js', params)
response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params)

bend_lng = response.json()['results'][0]['geometry']['location']['lng']
bend_lat = response.json()['results'][0]['geometry']['location']['lat']

      # src="https://maps.googleapis.com/maps/api/js?
      # key=AIzaSyAz83UxlsxZMPJCsl7ie2ZWj9ueKIpkwi0&
      # callback=initMap&l
      # ibraries=&v=weekly"

# >>> bend_lat
# 44.0581728
# >>> bend_lng
# -121.3153096

