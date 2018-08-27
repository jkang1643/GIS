import requests
#--------------------------------------------------------------------------------------------------
#INPUTS

#1 = block level, 2 = tract level, 3 = zipcode, 4 = public area microdata, 5 = metropolitan area
config = 4
street = "371 Tealwood Dr."
city = "Houston"
state = "TX"


#get GEOCODE Data, latitude, longitude, tract, block level census data
web_scrape_url = 'https://geocoding.geo.census.gov/geocoder/geographies/address?'

params = {
    'benchmark': 'Public_AR_Current',
    'vintage':'Current_Current',
    'street': street,
    'city': city,
    'state': state,
    'format':'json',
    'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
}

# Do the request and get the response data
req = requests.get(web_scrape_url, params=params)
str = req.json()
dictionary = (str['result']['addressMatches'])
dictionary = (dictionary[0])
dictionary_geo = (dictionary['geographies']['2010 Census Blocks'][0])


#dictionary items
latitude = (dictionary['coordinates']['x'])
longitude = (dictionary['coordinates']['y'])
zipcode = (dictionary['addressComponents']['zip'])
geo_id = (dictionary_geo['GEOID'])
block_name = (dictionary_geo['NAME'])
block_group = (dictionary_geo['BLKGRP'])
block_land_area = (dictionary_geo['AREALAND'])
block_water_area = (dictionary_geo['AREAWATER'])
state_blkgrp = (dictionary_geo['BLKGRP'])
state_id = (dictionary_geo['STATE'])
county_id = (dictionary_geo['COUNTY'])
tract_id = (dictionary_geo['TRACT'])


#--------------------------------------------------------------------------------------------------

#get Metropolitcan Statististical Area Code

web_scrape_url2 = 'https://geocoding.geo.census.gov/geocoder/geographies/address?'
params2 = {
    'benchmark': 'Public_AR_Current',
    'vintage': 'Current_Current',
    'street': street,
    'city': city,
    'state': state,
    'format': 'json',
    'layers': '80',
    'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
}
# Do the request and get the response data
req2 = requests.get(web_scrape_url2, params=params2)

#parse JSON response, because it is a multilayered dict
str2parse = req2.json()
str2parse = str2parse['result']['addressMatches']
str2 = str2parse[0]
str2 = dict(str2['geographies']['Metropolitan Statistical Areas'][0])


#assign variables to dict
msa_Name = str2["NAME"]
metropolitan_id = str2["CBSA"]
#-------------------------------------------------------------------------------------------------

#Get 2010 Census Public Use Microdata Areas
web_scrape_url3 = 'https://geocoding.geo.census.gov/geocoder/geographies/address?'
params3 = {
    'benchmark': 'Public_AR_Current',
    'vintage': 'Current_Current',
    'street': street,
    'city': city,
    'state': state,
    'format': 'json',
    'layers': '0',
    'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
}
# Do the request and get the response data
req3 = requests.get(web_scrape_url3, params=params3)
str3parse = req3.json()

#parse multi layered dictionary
str3parse1 = str3parse['result']['addressMatches'][0]
str3 = str3parse1['geographies']['2010 Census Public Use Microdata Areas'][0]
str3 = dict(str3)


#assign variables for microdata
microdata_id = str3["PUMA"]
microdata_area_name = str3["NAME"]
#-------------------------------------------------------------------------------------------------

#census ACS 5 year variables

#B25001_001E - total housing units
#B25002_002E - total occupied units
#B25002_003E - total vacant units
#B25106_024E - estimate total renter occupied housing units
#B01003_001E - total population in census tract
#B01002_001E - median age in tract
#B08013_001E - aggregate travel time to work
#B15012_001E - total fields of bachelers degrees reported
#B19049_001E - #Median household income in the past 12 months (in 2016 inflation-adjusted dollars)
#B19083_001E - GINI index of income inequality
#B25046_001E - aggregate number of vehicles available
#B25076_001E - lower quartile house value
#B25077_001E - median house value
#B25078_001E - upper quartile house value
#B25064_001E - estimate median gross rent
#B25057_001E - estimate lower quartile rent
#B25058_001E - median contract rent
#B25059_001E - estimate upper quartile rent

web_scrape_url = ['https://api.census.gov/data/2016/acs/acs5?']
get_statistics = ['NAME,'
                  'B25001_001E,'    #total housing units
                  'B25002_002E,'    #total occupied units
                  'B25002_003E,'    #total vacant units
                  'B25106_024E,'    #estimate total renter occupied housing units
                  'B01003_001E,'    #total population in census tract
                  'B01002_001E,'    #median age in tract
                  'B08013_001E,'    #aggregate travel time to work
                  'B15012_001E,'    #total fields of bachelers degrees reported
                  'B19049_001E,'    #Median household income in the past 12 months (in 2016 inflation-adjusted dollars)
                  'B19083_001E,'    #GINI index of income inequality
                  'B25046_001E,'    #aggregate number of vehicles available
                  'B25076_001E,'    #lower quartile house value
                  'B25077_001E,'    #median house value
                  'B25078_001E,'    #upper quartile house value
                  'B25064_001E,'    #estimate median gross rent
                  'B25057_001E,'    #estimate lower quartile rent
                  'B25058_001E,'    #median contract rent
                  'B25059_001E'     #estimate upper quartile rent
    ]



for x in web_scrape_url:
    #census tract level
    censusparams1 = {
        'get': get_statistics,
        'for': 'tract:' + tract_id,
        'in': 'state:' + state_id + ' county:' + county_id,
        'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }

    #census block level
    censusparams2 = {
        'get': get_statistics,
        'for': 'block group:' + block_group,
        'in': 'state:' + state_id + ' county:' + county_id + ' tract:' + tract_id,
        'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }

    #zipcode level
    censusparams3 = {
        'get': get_statistics,
        'for': 'zip code tabulation area:' + zipcode,
        'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }
    #public use microdata area
    censusparams4 = {
        'get': get_statistics,
        'for': 'public use microdata area:' + microdata_id,
        'in': 'state:' + state_id,
        'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }

    # metropolitan statistical area
    censusparams5 = {
        'get': get_statistics,
        'for': 'metropolitan statistical area/micropolitan statistical area:' + metropolitan_id,
        'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }


    #configure which region to use
    if config == 1:
        parameter = censusparams2
    elif config == 2:
        parameter = censusparams1
    elif config ==3:
        parameter = censusparams3
    elif config ==4:
        parameter = censusparams4
    else:
        parameter = censusparams5


    # Do the request and get the response data
    req = requests.get(x, params=parameter)
    res = req.json()
    results = res[1]
    print(results)

    #parse census results by numerical index
    census_name = results[0]
    total_housing_units = int(results[1])
    total_occupied_units = int(results[2])
    total_vacant_units = int(results[3])
    total_renter_occupied_units = int(results[4])
    total_population = results[5]
    median_age = results[6]
    aggregate_travel_time_to_work = results[7]
    total_fields_of_bachelors = results[8]
    median_household_income_past12 = results[9]
    GINI_inequality_index = results[10]
    aggregate_vehicles = results[11]
    lower_quartile_house_value = results[12]
    median_house_value = results[13]
    upper_quartile_house_value = results[14]
    median_gross_rent = results[15]
    lower_quartile_rent = results[16]
    median_contract_rent = results[17]
    upper_quartile_rent = results[18]


    #display results, to be used for dashboard
    print("Data Results for:" + census_name)
    print("Microdata Area Name:", microdata_area_name)
    print("Metropolitan Statistical Area Name:",msa_Name)
    print("Total Housing Units:",total_housing_units)
    print("Total Population:",total_population)
    print("Percent Occupied Units:",round((total_occupied_units/total_housing_units)*100,2),"%")
    print("Percent Vacant Units:",round((total_vacant_units/total_housing_units)*100,2),"%")
    print("Percent Rented Units:",round((total_renter_occupied_units/total_housing_units)*100,2),"%")
    print("Median Age:", median_age)
    print("Median Household Income:",median_household_income_past12)
    print("House Value(lower 25%, median, upper 25%):" + lower_quartile_house_value, median_house_value, upper_quartile_house_value)
    print("Rent(lower 25%, median, upper 25%):" + lower_quartile_rent, median_contract_rent, upper_quartile_rent)
