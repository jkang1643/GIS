import urllib.request
import urllib
from bs4 import BeautifulSoup
import numpy as np
import re
import datetime
import os
import requests

forty_two_floors = 'https://42floors.com/research'

page_scrape = urllib.request.urlopen(forty_two_floors)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page_scrape, 'html.parser')
# find city links to scrape

result = []
data = soup.findAll('div',attrs={'class':'uniformNav -vertical'})
for div in data:
    links = div.findAll('a')
    for a in links:
        links_string = ('https://42floors.com/' + a['href'])
        result.append(links_string)
result = result[15:]

print(result)
#----------------------------------------------------------------------------------------------------

for propertytype_box in soup.find_all('div', class_='uniformNav -vertical'):
    property_type = np.nan
    property_type = propertytype_box.text.replace('  ', '').replace('\n ', ',').replace('\n', '').strip()
property_type_index = property_type.split(",")

print(property_type_index)


#takes list of urls, searches csv

'''for each in result:
    html = requests.get(each)
    soup = BeautifulSoup(html.text, "html.parser")

    for link in soup.find_all('a', href=True):
        href = link['href']

        if any(href.endswith(x) for x in ['.csv']):
            print(href)'''


#make datetime a string
fmt = '%Y%m%d%H%M%S' # ex. 20110104172008 -> Jan. 04, 2011 5:20:08pm
now_str = datetime.datetime.now().strftime(fmt)
now_datetime = datetime.datetime.strptime(now_str, fmt)
date_time_export = str(now_datetime)
date_time_export = date_time_export.replace(" ", "_").replace(":","_")

#export unique timestamp for all data
baseDir = 'C:/Users/Joe/Documents/42Floors/' + date_time_export

n=0 #linked the two lists together using index change
for x in property_type_index:
    os.makedirs(os.path.join(baseDir,x),exist_ok=True)

    html = requests.get(result[n])
    soup = BeautifulSoup(html.text, "html.parser")
    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(href.endswith(x) for x in ['.csv']):
            print(href)
            name = href.split('/')[-1]
            print(name)
            print('waiting...')
            remote_file = requests.get('https://42floors.com/' + href)
            with open(os.path.join(baseDir,x,name), 'wb') as f:
                print('downloading...')
                for chunk in remote_file.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print('saved: ' + name)
    n += 1




