import requests
from ast import literal_eval

web_scrape_url = 'https://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?'

params = {
    'apiKey': '2aa4ba80051b489c9aa865ff0f6d5a28',
    'version': '4.01',
    'streetAddress': '35 Greycliff Rd.',
    'city': 'Boston ',
    'state': 'MA',
    'census': 'true',
    'censusYear':'2010',
}
# Do the request and get the response data
req = requests.get(web_scrape_url, params=params)
res = req.content
#parse string and decode
string = res.decode("ISO-8859-1")
var_array = string.split(',')

longitude = (var_array[3])
latitude = (var_array[4])
census_block = (var_array[40])
GEO_id_2 =(var_array[50]+var_array[43]+var_array[42].replace(".","")+var_array[41])

print(longitude,latitude,census_block,GEO_id_2)