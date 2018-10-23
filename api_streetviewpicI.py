import requests
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import json

#produce streetview of property

radius_numbers = [50, 1000, 5000, 50000]

for x in radius_numbers:
    web_scrape_url = 'https://maps.googleapis.com/maps/api/streetview?'
    params = {
        'size': '1200x600',
        'location':'29.765427,-95.54863',
        'fov' : '120',
        'radius' : x,
        'key':'AIzaSyAEEIuRKOBNzOjMADj4hE5bGUdAFKz9oDE'
}


    # Do the request and get the response data
    req = requests.get(web_scrape_url, params=params)
    if req.status_code == 200:
        with open("C:/Users/Joe/Desktop/sample" + str(x) + ".jpg", 'wb') as f:
            f.write(req.content)


#produce static map of property

web_scrape_url2 = 'https://maps.googleapis.com/maps/api/staticmap?'
params2 = {
    'size': '640x640',
    'center':'371 Tealwood Dr. Houston, TX',
    'zoom' : '16',
    'maptype' : 'roadmap',
    'markers' : 'size:medium|29.765427,-95.54863',
    'key':'AIzaSyAEEIuRKOBNzOjMADj4hE5bGUdAFKz9oDE'
}


# Do the request and get the response data
req2 = requests.get(web_scrape_url2, params=params2)
if req2.status_code == 200:
    with open("C:/Users/Joe/Desktop/samplemap.png", 'wb') as f:
        f.write(req2.content)



