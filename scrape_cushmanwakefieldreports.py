import urllib.request
import urllib
import urllib.parse
from bs4 import BeautifulSoup
import numpy as np
import re
import datetime
import os
import requests
from selenium import webdriver

web_scrape_search_terms = ['Atlanta', 'Austin', 'Baltimore', 'Birmingham', 'Boston', 'Buffalo',
                           'Charlotte', 'Chicago', 'Cincinnati', 'Cleveland', 'Columbus', 'Dallas',
                           'Denver', 'Detroit', 'Fairfield', 'Fresno', 'Grand Rapids', 'Hartford',
                           'Houston', 'Indianapolis', 'Jacksonville', 'Jersey City', 'Kansas City',
                           'Las Vegas', 'Los Angeles', 'Louisville', 'Memphis', 'Miami', 'Milwaukee',
                           'Minneapolis', 'Nashville', 'New Orleans', 'New York City', 'Newark',
                           'Oakland', 'Oklahoma City', 'Omaha', 'Orlando', 'Palm Beach', 'Philadelphia',
                           'Phoenix', 'Pittsburgh', 'Portland', 'Raleigh', 'Richmond', 'Rochester',
                           'Sacramento', 'Salt Lake City', 'San Antonio', 'San Diego', 'San Francisco',
                           'Seattle', 'Silicon Valley', 'Tampa Bay', 'Tucson', 'Virginia Beach',]


for query in web_scrape_search_terms:
    query = query.replace(" ", "%20")
    # Constracting http query
    url = r'http://www.cushmanwakefield.us/en/search-results?q='+query
    browser = webdriver.Chrome()  # replace with .Firefox(), or with the browser of your choice
    browser.get(url)  #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, 'html.parser')
    data = soup.find('div', attrs={'class': 'm-box m-box_nav m-box_search'})
    for a in data.find_all('a', attrs={'id': 'upperleftcolumn_0_rptFacet_hlLink_2'}):
        link = (r'http://www.cushmanwakefield.us' + a['href'])
        print(link) #outer loop to find marketbeat reports on sidebar"

        ##this is the inner loop that examines the specific files in marketbeat"
        browser2 = webdriver.Chrome()
        browser2.get(link)
        innerHTML2 = browser2.execute_script("return document.body.innerHTML")
        soup2 = BeautifulSoup(innerHTML2, 'html.parser')

        data2 = soup2.find('div', attrs={'class': 'bodyContent'})
        for a2 in data2.find_all('a', href=True):
            link2 = (r'http://www.cushmanwakefield.us' + a2['href'])
            print(link2)






