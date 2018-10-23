from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver

web_scrape_search_terms = ['Atlanta', 'Austin', 'Baltimore', 'Birmingham', 'Boston', 'Buffalo',
                           'Charlotte', 'Chicago', 'Cincinnati','Cleveland', 'Columbus', 'Dallas',
                           'Denver', 'Detroit', 'Fairfield', 'Fresno', 'Grand Rapids', 'Hartford',
                           'Houston', 'Indianapolis', 'Jacksonville', 'Jersey City', 'Kansas City',
                           'Las Vegas', 'Los Angeles', 'Louisville', 'Memphis', 'Miami', 'Milwaukee',
                           'Minneapolis', 'Nashville', 'Oklahoma City', 'Omaha', 'Orlando', 'Palm Beach',
                           'Philadelphia', 'Phoenix', 'Pittsburgh', 'Portland', 'Raleigh', 'Richmond', 'Rochester',
                           'Sacramento', 'Salt Lake City', 'San Antonio', 'San Diego', 'San Francisco',
                           'Seattle', 'Silicon Valley', 'Tampa Bay', 'Tucson',
                           'Virginia Beach', 'Washington D.C', "West Palm Beach"]


#'Atlanta', 'Austin', 'Baltimore', 'Birmingham', 'Boston', 'Buffalo', 'Charlotte', 'Chicago', 'Cincinnati','Cleveland', 'Columbus', 'Dallas','Denver', 'Detroit', 'Fairfield', 'Fresno', 'Grand Rapids', 'Hartford', 'Houston', 'Indianapolis', 'Jacksonville', 'Jersey City', 'Kansas City','Las Vegas', 'Los Angeles', 'Louisville', 'Memphis', 'Miami', 'Milwaukee','Minneapolis', 'Nashville', 'Oklahoma City', 'Omaha', 'Orlando', 'Palm Beach', 'Philadelphia', 'Phoenix', 'Pittsburgh

baseDir = 'C:/Users/Joe/Documents/CushmanWakefield/'
for query in web_scrape_search_terms:
    query1 = query.replace(" ", "%20")
    # Constracting http query
    url = r'http://www.cushmanwakefield.us/en/search-results?f={86FC8AB5-42C6-44A0-808B-B9FF6AAE4156}&q=' + query1

    ##this is the outer loop that examines the specific files in marketbeat"
    browser = webdriver.Chrome()
    browser.get(url)
    HTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(HTML, 'html.parser')

    minor_list = []

    data = soup.find('div', attrs={'class': 'bodyContent'})
    for a in data.find_all('a', href=True):
        link = (r'http://www.cushmanwakefield.us' + a['href'])
        minor_list.append(link)
    print(minor_list) #list of links to scrape by city

    for item in minor_list:
        browser2 = webdriver.Chrome()
        browser2.get(item)
        HTML2 = browser2.execute_script("return document.body.innerHTML")
        soup2 = BeautifulSoup(HTML2, 'html.parser')

        data = soup2.find('div', attrs={'class': 'm-box highlight lightGrey'})
        for link in soup2.find_all('a', href=True):
            href = link['href']
            if any(href.endswith(x) for x in ['.pdf']):
                print(href)
                file_name = href.split('/')[-1]
                print(file_name)
                print(file_name)
                remote_file = requests.get(href)
                os.makedirs(os.path.join(baseDir, query), exist_ok=True)
                with open(os.path.join(baseDir,query,file_name), 'wb') as f:
                    for chunk in remote_file.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print('saved: ' + href)




