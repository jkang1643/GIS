import requests
from urllib.parse import quote


payload = {'address':'371 tealwood dr houston '}

newpayload = {}
for (k, v) in payload.items():
    newpayload[quote(k)] = quote(v)

print(newpayload['address'])


base_url = 'http://api.walkscore.com/score?format=json&address='
latitude = '29.765395'
longitude = '-95.548624'
rest_url = '&transit=1&bike=1&wsapikey=723603e4e9ed1c836fb0403145a39cfc'
json_url = base_url + newpayload['address'] + "&" + "lat=" + latitude + "&lon=" + longitude + rest_url

response = requests.get(json_url)
data = response.json()

walk_score = (data['walkscore'])
walk_description = (data['description'])
transit_score = (data['transit']['score'])
transit_description = (data['transit']['description'])
bike_score = (data['bike']['score'])
bike_description = (data['bike']['description'])


print(data)