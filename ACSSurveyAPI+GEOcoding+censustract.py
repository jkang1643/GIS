import requests
import json
#--------------------------------------------------------------------------------------------------
#1 = tract level, 2 = block level
config = 1


web_scrape_url = 'https://geocoding.geo.census.gov/geocoder/geographies/address?'
params = {
    'benchmark': 'Public_AR_Current',
    'vintage':'Current_Current',
    'street': '371 Tealwood Dr',
    'city': 'Houston',
    'state': 'TX',
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

web_scrape_url = 'https://api.census.gov/data/2016/acs/acs5?'

#census tract level
params = {
    'get': 'NAME,B25001_001E,B25002_002E,B25002_003E,B25106_024E,B01003_001E,B01002_001E,B08013_001E,B15012_001E,B19049_001E,B19083_001E,B25046_001E,B25076_001E,B25077_001E,B25078_001E,B25064_001E,B25057_001E,B25058_001E,B25059_001E',
    'for': 'tract:' + tract_id,
    'in': 'state:' + state_id + ' county:' + county_id,
    'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
}

#census block level
params2 = {
    'get': 'NAME,B25001_001E,B25002_002E,B25002_003E,B25106_024E,B01003_001E,B01002_001E,B08013_001E,B15012_001E,B19049_001E,B19083_001E,B25046_001E,B25076_001E,B25077_001E,B25078_001E,B25064_001E,B25057_001E,B25058_001E,B25059_001E',
    'for': 'block group:' + block_group,
    'in': 'state:' + state_id + ' county:' + county_id + ' tract:' + tract_id,
    'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
}


if config == 1:
    parameter = params
else:
    parameter = params2


# Do the request and get the response data
req = requests.get(web_scrape_url, params=parameter)
res = req.json()
results = res[1]
print(results)

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


print("Results for:" + census_name)
print("Total Housing Units:",total_housing_units)
print("Total Population:",total_population)
print("Percent Occupied Units:",round((total_occupied_units/total_housing_units)*100,2),"%")
print("Percent Vacant Units:",round((total_vacant_units/total_housing_units)*100,2),"%")
print("Percent Rented Units:",round((total_renter_occupied_units/total_housing_units)*100,2),"%")
print("Median Age:", median_age)
print("Median Household Income:",median_household_income_past12)
print("House Value(lower 25%, median, upper 25%):" + lower_quartile_house_value, median_house_value, upper_quartile_house_value)
print("Rent(lower 25%, median, upper 25%):" + lower_quartile_rent, median_contract_rent, upper_quartile_rent)
