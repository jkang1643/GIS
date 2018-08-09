from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
import pandas as pd
import csv
import re
import numpy as np
import requests
from urllib.parse import quote

page_scrape = urllib.request.urlopen('https://42floors.com/us/ma/athol/2154-main-st?listing=1249165')

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page_scrape, 'html.parser')


#KEEP
extraslist = {}
for details_box in soup.find_all('div', class_='col-6 col-4-md margin-bottom'):
    for each in details_box.find_all("div", {"class": "text-bold"}):
        label = re.sub('[^a-zA-Z]+', '', each.string)
        label = re.compile('[\W_]+').sub(' ', label)
    for each in details_box.find_all("div", {"class": "strong"}):
        number = re.sub('[^0-9]', '', each.string)
        number = re.compile('[\W_]+').sub(' ', number)
    if label!='CloseHighways':
        extraslist[label] = number

print(extraslist)
print(extraslist['TotalSize'])