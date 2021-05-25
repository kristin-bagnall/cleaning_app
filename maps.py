import requests
import secrets
import json
from pprint import pprint

params = {"key": secrets.GOOGLE_API_KEY, 
          "address": "Bend, OR"}

# response = requests.get('https://maps.googleapis.com/maps/api/js', params)
response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params)


      # src="https://maps.googleapis.com/maps/api/js?
      # key=AIzaSyAz83UxlsxZMPJCsl7ie2ZWj9ueKIpkwi0&
      # callback=initMap&l
      # ibraries=&v=weekly"