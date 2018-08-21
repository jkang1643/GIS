import requests
import json

web_scrape_url = 'https://geocoding.geo.census.gov/geocoder/geographies/address?'
params = {
    'benchmark': 'Public_AR_Current',
    'vintage':'Current_Current',
    'street': '35 Greycliff Rd.',
    'city': 'Boston ',
    'state': 'MA',
    'format':'json',
    'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
}

# Do the request and get the response data
req = requests.get(web_scrape_url, params=params)
str = req.json()
dictionary = (str['result']['addressMatches'])
dictionary = (dictionary[0])
dictionary_geo = (dictionary['geographies']['2010 Census Blocks'][0])

print(dictionary)
print(dictionary_geo)

#dictionary items
latitude = (dictionary['coordinates']['x'])
longitude = (dictionary['coordinates']['y'])
zipcode = (dictionary['addressComponents']['zip'])
geo_id = (dictionary_geo['GEOID'])
block_name = (dictionary_geo['NAME'])
block_group = (dictionary_geo['BLKGRP'])
block_land_area = (dictionary_geo['AREALAND'])
block_water_area = (dictionary_geo['AREAWATER'])
state_blkgrp = (dictionary_geo['BLKGRP'])
state_id = (dictionary_geo['STATE'])
county_id = (dictionary_geo['COUNTY'])
tract_id = (dictionary_geo['TRACT'])

print(state_blkgrp,state_id,county_id,tract_id)