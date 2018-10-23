#changes vs. realestatemasterdata =
#1. added the url parse instead of scraping address for increased accuracy
#2. added the onelineaddress option instead of by part for the geocoding API by US Census
#3. relieved address city state from web scraping duties
#4. read data from property by column index instead of "listing_url"

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
import sys
import time

#downloading all CSV files from 42 floors and saving the name as the retrieve date
#-----------------------------------------------------------------------------------

#opening the CSV and reading the columns
#--------------------------------------------------------------------------------------
CSV_location_file = 'C:/Users/Joe/Documents/42Floors/2018-08-08_23_12_24/Austin/property_data.csv'


with open(CSV_location_file, newline='', encoding="utf8") as f:
    reader = csv.reader(f)
    my_list = list(reader)
#print(my_list)


df = pd.read_csv(CSV_location_file)
saved_column = df[df.columns[10]]
print(saved_column)
URL_list = []

for x in saved_column:
    URL_list.append(x)

print(URL_list)

#scraping the website part
#--------------------------------------------------------------------------------------
#for row in URL_list:
def getURLlist(row):

    try:
        walk_score = np.nan
        walk_description = np.nan
        transit_score = np.nan
        transit_description = np.nan
        bike_score = np.nan
        bike_description = np.nan

        # parse the URL for address city state instead of scraping
        row_split = (row.split("/"))
        full_address = row_split[6] + " " + row_split[5] + " " + row_split[4]
        full_address = (full_address.replace("-", " "))
        unparsed_address = row_split[6]
        address = unparsed_address.replace("-", " ")
        city = row_split[5]
        state = row_split[4]

        # for each URL, go to website, scrape data, obtain longitude latitute, then use that to obtain
        # walkability, census information, census block data, and append to CSV write

        #--------------------[SCRAPE THE URL}-------------------------------------------------------------
        page_scrape = urllib.request.urlopen(row)


        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page_scrape, 'html.parser')


        # find square foot
        sqfoot_box = soup.find('div', attrs={"class": 'listing-size col-5-sm col-3-md'})
        sqfoot = np.nan
        sqfoot1 = re.compile('[\W_]+').sub('', sqfoot_box.text)
        sqfoot = float(re.sub('[a-z]', '', sqfoot1))



        #find listing rate
        listing_rate_box = soup.find('div', attrs={"class": 'listing-rate col-2-md hide-sm '})
        listing_rate = np.nan
        listing_rate_unfiltered=re.compile('[\W_]+').sub('', listing_rate_box.text)


        if "sqft" in listing_rate_unfiltered:
            listing_rate = float(re.sub('[a-z]', '', listing_rate_unfiltered))/100
        elif "mo" in listing_rate_unfiltered:
            listing_rate = float(re.sub('[a-z]', '', listing_rate_unfiltered))
        else:
            raise ValueError('A very specific bad thing happened')



        # find property type
        try:
            for propertytype_box in soup.find_all('div', class_= 'tags margin-bottom text-small'):
                property_type = np.nan
                property_type = re.compile('[\W_]+').sub(' ', propertytype_box.text)
        except:
            pass


        # find original listing date
        t = soup.find('span', {'class': 'text-nowrap text-bold'})
        listing_date = t.text


        #(details box)
        for detail_box in soup.find_all('div', class_= 'grid grid-nest grid-top'):
            details = np.nan
            details = re.compile('[\W_]+').sub(',', detail_box.text)


        #parse the details box by dictionary index and name [includes all the extra features]
        extraslist = {}
        for details_box in soup.find_all('div', class_='col-6 col-4-md margin-bottom'):
            for each in details_box.find_all("div", {"class": "text-bold"}):
                extras_label = re.sub('[^a-zA-Z]+', '', each.string)
                extras_label = re.compile('[\W_]+').sub(' ', extras_label)
            for each in details_box.find_all("div", {"class": "strong"}):
                extras_number = re.sub('[^0-9a-zA-Z:]', '', each.string)
                extras_number = re.compile('[\W_]+').sub(' ', extras_number)
            if extras_label != 'CloseHighways':
                extraslist[extras_label] = extras_number


        print(extraslist)

        floors = np.nan
        try:
            floors = extraslist['Floors']
        except:
            pass

        TotalSize = np.nan
        try:
            TotalSize = extraslist['TotalSize']
        except:
            pass

        LotSize = np.nan
        try:
            LotSize = extraslist['LotSize']
        except:
            pass

        YearConstructed = np.nan
        try:
            YearConstructed = extraslist['YearConstructed']
        except:
            pass


        BuildingClass = np.nan
        try:
            BuildingClass = extraslist['BuildingClass']
        except:
            pass


        Zoning = np.nan
        try:
            Zoning = extraslist['Zoning']
        except:
            pass

        ParkingRatio = np.nan
        try:
            ParkingRatio = extraslist['ParkingRatio']
        except:
            pass


#-----------------[obtain longitude latitude coordinates for each data point]--------------------------
#------------------------------------------------------------------------------------------------------

        web_scrape_url = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?'
        params = {
            'benchmark': 'Public_AR_Current',
            'vintage': 'Current_Current',
            'address': full_address,
            'format': 'json',
            'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
        }

        # Do the request and get the response data
        starttime = time.time()
        while True:
            try:
                if time.time() - starttime > 30.:
                    print('ERROR: Timeout 10s')
                    break
                req = requests.get(web_scrape_url, params=params)
                str = req.json()
                print(str)
                dictionary = (str['result']['addressMatches'])
                dictionary = (dictionary[0])
                dictionary_geo = (dictionary['geographies']['2010 Census Blocks'][0])
                break
            except:
                continue
        # dictionary items
        latitude = (dictionary['coordinates']['y'])
        longitude = (dictionary['coordinates']['x'])
        latitude = "{:.6f}".format(latitude)
        longitude = "{:.6f}".format(longitude)
        zipcode = (dictionary['addressComponents']['zip'])
        geo_id = (dictionary_geo['GEOID'])
        block_name = (dictionary_geo['NAME'])
        block_group = (dictionary_geo['BLKGRP'])
        block_land_area = (dictionary_geo['AREALAND'])
        block_water_area = (dictionary_geo['AREAWATER'])


# -----------------[use longitude latitude coordinates to obtain census data]---------------------
#-------------------------------------------------------------------------------------------------
        web_scrape_url = 'https://www.broadbandmap.gov/broadbandmap/demographic/2014/coordinates?'

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'format': "json"
        }

        # Do the request and get the response data
        req = requests.get(web_scrape_url, params=params)
        data = req.json()

        income_below_poverty = (data['Results']['incomeBelowPoverty'])
        median_income = (data['Results']['medianIncome'])
        income_less_25 = (data['Results']['incomeLessThan25'])
        income_between_25_and_50 = (data['Results']['incomeBetween25to50'])
        income_between_50_and_100 = (data['Results']['incomeBetween50to100'])
        income_between_100_and_200 = (data['Results']['incomeBetween100to200'])
        income_greater_200 = (data['Results']['incomeGreater200'])
        highschool_graduation_rate = (data['Results']['educationHighSchoolGraduate'])
        college_education_rate = (data['Results']['educationBachelorOrGreater'])


#----------------[obtain walkability, bike, and travel scores by location}----------------------------
#----------------------------------------------------------------------------------------------------

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


        output = (listing_date, latitude, longitude, geo_id, block_name, block_group, address, city, zipcode, state, walk_score,
                  walk_description, transit_score, transit_description, bike_score, bike_description, sqfoot,
                  listing_rate, property_type, details, floors, TotalSize, LotSize, ParkingRatio, YearConstructed, BuildingClass, Zoning, median_income, income_below_poverty, income_less_25,
                  income_between_25_and_50, income_between_50_and_100, income_between_100_and_200, income_greater_200,
                  highschool_graduation_rate, college_education_rate, row)

#--------------------------------[PRINTING AND EXPORTING]----------------------------------------------


        print(listing_date, latitude, longitude, geo_id, block_name, block_group, address, city, state, zipcode, walk_score, walk_description, transit_score, transit_description, bike_score, bike_description, sqfoot, listing_rate, property_type, details, floors, TotalSize, LotSize, ParkingRatio, YearConstructed, BuildingClass, Zoning, median_income, income_below_poverty, income_less_25, income_between_25_and_50, income_between_50_and_100, income_between_100_and_200, income_greater_200, highschool_graduation_rate, college_education_rate, row)

        with open('aust.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(output)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, row)


#-----------------------------[Added multithreading capabilities]--------------------------------------
#multithreading
if __name__ == "__main__":
    #pool = ThreadPool(12)
    #results = pool.map(getURLlist, URL_list)
    #pool.close()
    #pool.join()
#multipooling
    with mp.Pool(os.cpu_count()) as p:
        results = p.map_async(getURLlist, URL_list)
        p.close()
        p.join()
