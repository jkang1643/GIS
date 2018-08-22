import requests

web_scrape_url = 'https://geocoding.geo.census.gov/geocoder/geographies/address?'

params2 = {
    'benchmark': 'Public_AR_Current',
    'vintage': 'Current_Current',
    'street': '371 Tealwood Dr',
    'city': 'Houston',
    'state': 'TX',
    'format': 'json',
    'layers': '80',
    'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
}

# Do the request and get the response data
req = requests.get(web_scrape_url, params=params2)
str = req.json()
str = str['result']['addressMatches']
print(str)