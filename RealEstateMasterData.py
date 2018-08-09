from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import pandas as pd
import csv
import re
import numpy as np
import requests
from urllib.parse import quote
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing as mp
import os

#downloading all CSV files from 42 floors and saving the name as the retrieve date
#-----------------------------------------------------------------------------------

#opening the CSV and reading the columns
#--------------------------------------------------------------------------------------

CSV_location_file = '42floors-listing_data-us-md-greater-baltimore-as-of-Aug-03.csv'

with open(CSV_location_file, newline='') as f:
    reader = csv.reader(f)
    my_list = list(reader)
#print(my_list)

df = pd.read_csv(CSV_location_file)
saved_column = df.listing_url
print(saved_column)

URL_list = []

for x in saved_column:
    URL_list.append(x)

print(URL_list)

#scraping the website part
#--------------------------------------------------------------------------------------

def getURLlist(row):

#for row in URL_list:
    try:
        walk_score = np.nan
        walk_description = np.nan
        transit_score = np.nan
        transit_description = np.nan
        bike_score = np.nan
        bike_description = np.nan

        page_scrape = urllib.request.urlopen(row)

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page_scrape, 'html.parser')
        # find square foot
        sqfoot_box = soup.find('div', attrs={"class": 'listing-size col-5-sm col-3-md'})
        sqfoot = np.nan
        sqfoot = re.compile('[\W_]+').sub('', sqfoot_box.text)
        #sqfoot = sqfoot_box.text.replace('\n', ' ').replace('  ', ' ').strip()  # strip() is used to remove starting and trailing

        #find address
        address_box = soup.find('h1', attrs={"class": 'bold margin-none'})
        address = np.nan
        address = address_box.text.replace('\n', ' ').replace('  ', ' ').strip()  # strip() is used to remove starting and trailing

        #find listing rate
        listing_rate_box = soup.find('div', attrs={"class": 'listing-rate col-2-md hide-sm '})
        listing_rate = np.nan
        listing_rate=re.compile('[\W_]+').sub('', listing_rate_box.text)


        # find property type
        for propertytype_box in soup.find_all('div', class_= 'tags margin-bottom text-small'):
            property_type = np.nan
            property_type = re.compile('[\W_]+').sub(' ', propertytype_box.text)


        #(details box)
        for detail_box in soup.find_all('div', class_= 'grid grid-nest grid-top'):
            details = np.nan
            details = re.compile('[\W_]+').sub(',', detail_box.text)

        # class="col-6 col-4-md margin-bottom"
        #for details_box in soup.find_all('div', class_='col-6 col-4-md margin-bottom'):

        location_box = soup.find('div', attrs={"class": 'address'})
        state_now = np.nan
        city_now = np.nan
        location_now=re.sub('[^a-zA-Z,]+', '', location_box.text)

        location_now_list=location_now.split(',')
        state = (location_now_list[-1])
        city = (location_now_list[-2])
        city = re.sub('([A-Z])', r' \1', city)[1:]

#obtain longitude latitude coordinates for each data point
#---------------------------------------------------------------------------------------

        web_scrape_url = 'https://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?'

        params = {
            'apiKey': '2aa4ba80051b489c9aa865ff0f6d5a28',
            'version': '4.01',
            'streetAddress': address,
            'city': city,
            'state': state,
            'census': 'true',
            'censusYear': '2010',
        }
        # Do the request and get the response data
        req = requests.get(web_scrape_url, params=params)
        res = req.content
        # parse string and decode
        string = res.decode("ISO-8859-1")
        var_array = string.split(',')

        latitude = (var_array[3])
        longitude = (var_array[4])
        census_block = (var_array[40])
        geo_id_2 = (var_array[50] + var_array[43] + var_array[42].replace(".", "") + var_array[41])

#obtain census data for each longitude latitude
#-------------------------------------------------------------------------------------------------

        base_url = 'https://www.broadbandmap.gov/broadbandmap/demographic/2014/coordinates?'
        json_url = base_url + "latitude=" + latitude + "&longitude=" + longitude + "&format=json"
        response = requests.get(json_url)

        data = response.json()

        income_below_poverty = (data['Results']['incomeBelowPoverty'])
        median_income = (data['Results']['medianIncome'])
        income_less_25 = (data['Results']['incomeLessThan25'])
        income_between_25_and_50 = (data['Results']['incomeBetween25to50'])
        income_between_50_and_100 = (data['Results']['incomeBetween50to100'])
        income_between_100_and_200 = (data['Results']['incomeBetween100to200'])
        income_greater_200 = (data['Results']['incomeGreater200'])
        highschool_graduation_rate = (data['Results']['educationHighSchoolGraduate'])
        college_education_rate = (data['Results']['educationBachelorOrGreater'])

#obtain walkability, bike, and travel scores by location
#---------------------------------------------------------------------------------------

        payload = {'address': address + " " + city + " " + state}

        newpayload = {}
        for (k, v) in payload.items():
            newpayload[quote(k)] = quote(v)

        base_url = 'http://api.walkscore.com/score?format=json&address='
        rest_url = '&transit=1&bike=1&wsapikey=723603e4e9ed1c836fb0403145a39cfc'
        json_url = base_url + newpayload['address'] + "&" + "lat=" + latitude + "&lon=" + longitude + rest_url

        response = requests.get(json_url)
        data = response.json()

        try:
            walk_score = (data['walkscore'])
        except:
            pass

        try:
            walk_description = (data['description'])
        except:
            pass

        try:
            transit_score = (data['transit']['score'])
        except:
            pass

        try:
            transit_description = (data['transit']['description'])
        except:
            pass

        try:
            bike_score = (data['bike']['score'])
        except:
            pass

        try:
            bike_description = (data['bike']['description'])
        except:
            pass

        output = (geo_id_2, census_block, latitude, longitude, address, city, state, walk_score, walk_description, transit_score, transit_description, bike_score, bike_description, sqfoot, listing_rate, property_type, details, median_income, income_below_poverty, income_less_25, income_between_50_and_100, income_between_100_and_200, income_greater_200, highschool_graduation_rate, college_education_rate, row)

        '''extraslist = {}
        for details_box in soup.find_all('div', class_='col-6 col-4-md margin-bottom'):
            for each in details_box.find_all("div", {"class": "text-bold"}):
                label = re.sub('[^a-zA-Z]+', '', each.string)
                label = re.compile('[\W_]+').sub(' ', label)
            for each in details_box.find_all("div", {"class": "strong"}):
                number = re.sub('[^0-9]', '', each.string)
                number = re.compile('[\W_]+').sub(' ', number)
            if label != 'CloseHighways':
                extraslist[label] = number
        
        # repeat for every column you want from extras
        floors = np.nan
        try:
            floors = extraslist['Floors']
        except:
            pass
        output.append(floors)
        '''
#------------------------------------------------------------------------------------------------
#PRINTING AND EXPORTING

        print(geo_id_2, census_block, latitude, longitude, address, city, state, walk_score, walk_description, transit_score, transit_description, bike_score, bike_description, sqfoot, listing_rate, property_type, details, median_income, income_below_poverty, income_less_25, income_between_50_and_100, income_between_100_and_200, income_greater_200, highschool_graduation_rate, college_education_rate, row)

        with open('master.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(output)

    except:
        print('ERROR:',row)

#multithreading
if __name__ == "__main__":
    #pool = ThreadPool(12)
    #results = pool.map(getURLlist, URL_list)
    #pool.close()
    #pool.join()

    with mp.Pool(os.cpu_count()) as p:
        results = p.map_async(getURLlist, URL_list)
        p.close()
        p.join()