from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import re

page_scrape = urllib.request.urlopen('https://42floors.com/us/ma/athol/2154-main-st?listing=1249165')

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page_scrape, 'html.parser')

#KEEP
extraslist = {}
for details_box in soup.find_all('div', class_='col-6 col-4-md margin-bottom'):
    for each in details_box.find_all("div", {"class": "text-bold"}):
        extras_label = re.sub('[^a-zA-Z]+', '', each.string)
        extras_label = re.compile('[\W_]+').sub(' ', extras_label)
    for each in details_box.find_all("div", {"class": "strong"}):
        extras_number = re.sub('[^0-9]', '', each.string)
        extras_number = re.compile('[\W_]+').sub(' ', extras_number)
    if extras_label!='CloseHighways':
        extraslist[extras_label] = extras_number

print(extraslist)
print(extraslist['TotalSize'])

starttime = time.time()
while True:
    try:
        if time.time() - starttime > 60.:
            print('ERROR: Timeout 60s')
            break
        req = requests.get(web_scrape_url, params=params)
        str = req.json()
        dictionary = (str['result']['addressMatches'])
        dictionary = (dictionary[0])
        dictionary_geo = (dictionary['geographies']['2010 Census Blocks'][0])
        break
    except:
        continue