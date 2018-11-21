import requests


#get GEOCODE Data, latitude, longitude, tract, block level census data
web_scrape_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

params = {
    'address': '371 Tealwood Dr. Houston TX',
    'key':'AIzaSyAEEIuRKOBNzOjMADj4hE5bGUdAFKz9oDE'
}

# Do the request and get the response data
req = requests.get(web_scrape_url, params=params)
print(req)
str = req.json()
print(str)