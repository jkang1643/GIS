import requests
import pandas as pd
import numpy as np
import matplotlib
import cufflinks as cf
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

#--------------------------------------------------------------------------------------------------

#INPUTS


#1 = block level, 2 = tract level, 3 = zipcode, 4 = public area microdata, 5 = metropolitan area
config = 2
street = "35 Greycliff Rd"
city = "Boston"
state = "MA"



#------------------------------------------------------------------------------------------------

#get GEOCODE Data, latitude, longitude, tract, block level census data
web_scrape_url = 'https://geocoding.geo.census.gov/geocoder/geographies/address?'

params = {
    'benchmark': 'Public_AR_Current',
    'vintage':'Current_Current',
    'street': street,
    'city': city,
    'state': state,
    'format':'json',
    'key':'80a64bc7e2514da9873c3a235bd3fb59be140157'
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

print(str3parse1)

#------------------------------------------------------------------------------------------------------
#--------------------------[CENSUS ACS 5 Community Survey Data]----------------------------------------

#results[0:16]
summary = ['NAME,'
          'B25001_001E,'    #total housing units
          'B25002_002E,'    #total occupied units
          'B25002_003E,'    #total vacant units
          'B25106_024E,'    #estimate total renter occupied housing units
          'B01003_001E,'    #total population in census tract
          'B01002_001E,'    #median age in tract
          'B19049_001E,'    #Median household income in the past 12 months (in 2016 inflation-adjusted dollars)
          'B19083_001E,'    #GINI index of income inequality
          'B25076_001E,'    #lower quartile house value
          'B25077_001E,'    #median house value
          'B25078_001E,'    #upper quartile house value
          'B25064_001E,'    #estimate median gross rent
          'B25057_001E,'    #estimate lower quartile rent
          'B25058_001E,'    #median contract rent
          'B25059_001E'     #estimate upper quartile rent
    ]

#results[19:67]
demographics = ['B01001_002E,'    #Estimate!!Total!!Male   
                'B01001_003E,'    #Male!!Under 5 years        
                'B01001_004E,'    #Male!!5 to 9 years
                'B01001_005E,'    #Male!!10 to 14 years
                'B01001_006E,'    #Male!!15 to 17 years
                'B01001_007E,'    #Male!!18 and 19 years
                'B01001_008E,'    #Male!!20 years
                'B01001_009E,'    #Male!!21 years
                'B01001_010E,'    #Male!!22 to 24 years
                'B01001_011E,'    #Male!!25 to 29 years
                'B01001_012E,'    #Male!!30 to 34 years
                'B01001_013E,'    #Male!!35 to 39 years
                'B01001_014E,'    #Male!!40 to 44 years
                'B01001_015E,'    #Male!!45 to 49 years
                'B01001_016E,'    #Male!!50 to 54 years
                'B01001_017E,'    #Male!!55 to 59 years
                'B01001_018E,'    #Male!!60 and 61 years
                'B01001_019E,'    #Male!!62 to 64 years
                'B01001_020E,'    #Male!!65 and 66 years
                'B01001_021E,'    #Male!!67 to 69 years
                'B01001_022E,'    #Male!!70 to 74 years
                'B01001_023E,'    #Male!!75 to 79 years
                'B01001_024E,'    #Male!!80 to 84 years
                'B01001_025E,'    #Male!!85 years and over
                'B01001_026E,'    #Total!!Female
                'B01001_027E,'    #Female!!Under 5 years
                'B01001_028E,'    #Female!!5 to 9 years
                'B01001_029E,'    #Female!!10 to 14 years
                'B01001_030E,'    #Female!!15 to 17 years
                'B01001_031E,'    #Female!!18 and 19 years
                'B01001_032E,'    #Female!!20 years
                'B01001_033E,'    #Female!!21 years
                'B01001_034E,'    #Female!!22 to 24 years
                'B01001_035E,'    #Female!!25 to 29 years
                'B01001_036E,'    #Female!!30 to 34 years
                'B01001_037E,'    #Female!!35 to 39 years
                'B01001_038E,'    #Female!!40 to 44 years
                'B01001_039E,'    #Female!!45 to 49 years
                'B01001_040E,'    #Female!!50 to 54 years
                'B01001_041E,'    #Female!!55 to 59 years
                'B01001_042E,'    #Female!!60 and 61 years
                'B01001_043E,'    #Female!!62 to 64 years
                'B01001_044E,'    #Female!!65 and 66 years
                'B01001_045E,'    #Female!!67 to 69 years
                'B01001_046E,'    #Female!!70 to 74 years
                'B01001_047E,'    #Female!!75 to 79 years
                'B01001_048E,'    #Female!!80 to 84 years
                'B01001_049E'    #Female!!85 years and over
    ]

#results[70:79]
race = ['B01001H_001E,'     #white
        'B01001I_001E,'     #hispanic
        'B01001B_001E,'     #black
        'B01001D_001E,'     #asian
        'B01001C_001E,'     #native american/alaska native
        'B01001E_001E,'     #native hawaiian/pacific islander
        'B01001F_001E,'     #other
        'B01001G_001E,'      #two or more races
        'B02001_001E'       #total race
        ]

#results[82:123]
ethnicity1 = ['B04006_001E,'    #Total Reporting Ancestry
             'B04006_002E,'     #Afghan
             'B04006_003E,'     #Albanian
             'B04006_004E,'     #Alsatian     
             'B04006_005E,'     #American    
             'B04006_006E,'     #Arab     
             'B04006_016E,'     #Armenian
             'B04006_017E,'     #Assyrians
             'B04006_018E,'     #Australians
             'B04006_019E,'     #Austrian
             'B04006_020E,'     #Basque
             'B04006_021E,'     #Belgian
             'B04006_022E,'     #Brazilian
             'B04006_023E,'     #British
             'B04006_024E,'     #Bulgarian
             'B04006_025E,'     #Cajun
             'B04006_026E,'     #Canadian
             'B04006_027E,'     #Carpatho Rusyn
             'B04006_028E,'     #Celtic
             'B04006_029E,'     #Croatian
             'B04006_030E,'     #Cypriot
             'B04006_031E,'     #Czech
             'B04006_032E,'     #Czechoslovakian
             'B04006_033E,'     #Danish
             'B04006_034E,'     #Dutch
             'B04006_035E,'     #Eastern European
             'B04006_036E,'     #English
             'B04006_037E,'     #Estonian
             'B04006_038E,'     #European
             'B04006_039E,'     #Finnish
             'B04006_040E,'     #French
             'B04006_041E,'     #French Canadian
             'B04006_042E,'     #German 
             'B04006_043E,'     #German Russian
             'B04006_044E,'     #Greek
             'B04006_045E,'     #Guayanese
             'B04006_046E,'     #Hungarian
             'B04006_047E,'     #Icelander
             'B04006_048E,'     #Iranaian
             'B04006_049E,'     #Irish
             'B04006_050E'      #Israeli
        ]

#results[126:156]
ethnicity2 = ['B04006_051E,'    #Italian
              'B04006_052E,'    #Latvian
              'B04006_053E,'    #Lithuanian
              'B04006_054E,'    #Luxemburger
              'B04006_055E,'    #Macedonian
              'B04006_056E,'    #Maltese
              'B04006_057E,'    #New Zealander
              'B04006_058E,'    #Northern European
              'B04006_059E,'    #Norwegian
              'B04006_060E,'    #Pennsylvania German
              'B04006_061E,'    #Polish
              'B04006_062E,'    #Portuguese 
              'B04006_063E,'    #Romanian
              'B04006_064E,'    #Russian
              'B04006_065E,'    #Scandinavian
              'B04006_066E,'    #Scotch-Irish
              'B04006_067E,'    #Scottish
              'B04006_068E,'    #Serbian
              'B04006_069E,'    #Slavic
              'B04006_070E,'    #Slovak
              'B04006_071E,'    #Soviet Russia
              'B04006_072E,'    #Soviet Union
              'B04006_073E,'    #Subsaharan Africa
              'B04006_089E,'    #Swedish
              'B04006_090E,'    #Swiss
              'B04006_091E,'    #Turkish
              'B04006_092E,'    #Ukrainian
              'B04006_094E,'    #West Indian
              'B04006_107E,'    #Yugoslavian
              'B04006_108E'     #Estimate Other
]

#results[159:161]
foreign_native = ['B05012_002E,'    #Native
                  'B05012_003E'     #Foreign Born
                  ]

#results[164:170]
relationship = ['B06008_001E,'  #Total Count
                'B06008_002E,'  #Single/Never Married
                'B06008_003E,'  #Currently Married
                'B06008_004E,'  #Divorced
                'B06008_005E,'  #Separated
                'B06008_006E'   #Widowed
                ]

#results[173:179]
education = ['B06009_001E,'     #Total
             'B06009_002E,'     #Less Than High School Graduate
             'B06009_003E,'     #High School Graduate
             'B06009_004E,'     #Some College/Associates 
             'B06009_005E,'     #Bachelors Degree
             'B06009_006E'     #Graduate or professional degree
             ]

#results[182:192]
transportation = ['B08301_001E,'    #Total Means of Transportation
                  'B08301_003E,'    #Car, Van, Truck, Drove Alone
                  'B08301_004E,'    #Car, Van, Truck, Carpooled
                  'B08301_010E,'    #Used Public Transportation
                  'B08301_018E,'    #Bicycle
                  'B08301_019E,'    #Walked
                  'B08006_016E,'    #Taxicab
                  'B08301_017E,'    #Motorcycle
                  'B08301_020E,'    #Other Means
                  'B08301_021E'     #Worked at Home
                  ]

#results[195:210]
work = ['B08011_001E,'     #Total
             'B08011_002E,'     #12:00 a.m. to 4:59 a.m
             'B08011_003E,'     #5:00 a.m. to 5:29 a.m.
             'B08011_004E,'     #5:30 a.m. to 5:59 a.m. 
             'B08011_005E,'     #6:00 a.m. to 6:29 a.m.
             'B08011_006E,'     #6:30 a.m. to 6:59 a.m.
             'B08011_007E,'     #7:00 a.m. to 7:29 a.m.
             'B08011_008E,'     #7:30 a.m. to 7:59 a.m
             'B08011_009E,'     #8:00 a.m. to 8:29 a.m.
             'B08011_010E,'     #8:30 a.m. to 8:59 a.m.
             'B08011_011E,'     #9:00 a.m. to 9:59 a.m.
             'B08011_012E,'     #10:00 a.m. to 10:59 a.m.
             'B08011_013E,'     #11:00 a.m. to 11:59 a.m
             'B08011_014E,'     #12:00 p.m. to 3:59 p.m.
             'B08011_015E'     #4:00 p.m. to 11:59 p.m.
]

#results[213:226]
travel_time = ['B08012_001E,'     #Total
             'B08012_002E,'     #Less than 5 minutes
             'B08012_003E,'     #5 to 9 minutes
             'B08012_004E,'     #10 to 14 minutes 
             'B08012_005E,'     #15 to 19 minutes
             'B08012_006E,'     #20 to 24 minutes
             'B08012_007E,'     #25 to 29 minutes
             'B08012_008E,'     #30 to 34 minutes
             'B08012_009E,'     #35 to 39 minutes
             'B08012_010E,'     #40 to 44 minutes
             'B08012_011E,'     #45 to 59 minutes
             'B08012_012E,'     #60 to 89 minutes
             'B08012_013E'      #!90 or more minutes
]

#results[229:236]
vehicles = ['B08014_001E,'      #Total
            'B08014_002E,'      #No Vehicles
            'B08014_003E,'      #1 Vehicle 
            'B08014_004E,'      #2 Vehicles 
            'B08014_005E,'      #3 Vehicles
            'B08014_006E,'      #4 Vehicles
            'B08014_007E'       #5 or more Vehicles
            ]

#results[239:248]
worker_class = ['B08128_001E,'  #Total Worker Class
                'B08128_002E,'  #Employee of private company workers
                'B08128_003E,'  #Self-employed in own incorporated business workers
                'B08128_005E,'  #Private not-for-profit wage and salary workers
                'B08128_006E,'  #Local Government Workers
                'B08128_007E,'  #State Government workers
                'B08128_008E,'  #Federal Government Workers
                'B08128_009E,'  #Self-employed in own not incorporated business workers
                'B08128_010E'  #Unpaid family workers
                ]

#results[251:261]
under18 = ['B08301_021E,'       #Total
           'B09001_002E,'       #Total In Households
           'B09001_003E,'       #Households, Under 3
           'B09001_004E,'       #Households, 3-4 
           'B09001_005E,'       #5 years old
           'B09001_006E,'       #6-8 years old
           'B09001_007E,'       #9-11 years old
           'B09001_008E,'       #12-14 years old
           'B09001_009E,'       #15-17 years old
           'B09001_010E'        #In Group Quarters
           ]

#results[264:272]
school_enrollment = ['B14001_002E,'     #Total Enrolled in School
                     'B14001_003E,'     #Nursery School/Preschool
                     'B14001_004E,'     #Enrolled in kindergarten
                     'B14001_005E,'     #Enrolled Grades 1-4
                     'B14001_006E,'     #Enrolled Grades 5-8
                     'B14001_007E,'     #Enrolled Grades 9-12
                     'B14001_008E,'     #Enrolled in college, undergraduate years
                     'B14001_009E'      #Enrolled in Graduate School
                     ]

#results[275:291]
bachelors_field_study = ['B15012_001E,'     #Total
                         'B15012_002E,'     #Computers, Mathematics and Statistics
                         'B15012_003E,'     #Biological, Agricultural, and Environmental Sciences
                         'B15012_004E,'     #Physical and Related Sciences
                         'B15012_005E,'     #Psychology
                         'B15012_006E,'     #Social Sciences
                         'B15012_007E,'     #Engineering
                         'B15012_008E,'     #Multidisciplinary Studies
                         'B15012_009E,'     #Science and Engineering Related Fields
                         'B15012_010E,'     #Business
                         'B15012_011E,'     #Education
                         'B15012_012E,'     #Literature and Languages
                         'B15012_013E,'     #Liberal Arts and History
                         'B15012_014E,'     #Visual and Performing Arts	
                         'B15012_015E,'     #Communications
                         'B15012_016E'      #Other
                         ]

#results[294:301]
nativity_language = ['B16005_001E,'     #Estimate 
                     'B16005_002E,'     #Native
                     'B16005_003E,'     #Speak Only English
                     'B16005_004E,'     #Speak Spanish 
                     'B16005_009E,'     #Speak Indo-European Languages
                     'B16005_014E,'     #Speak Asian/Pacific Islander Language
                     'B16005_019E'      #Speak Other Language
]

#results[304:320]
household_income_past_12 = ['B19001_002E,'      #Less than $10,000
                    'B19001_003E,'      #$10,000 to $14,999
                    'B19001_004E,'      #15,000 to $19,999
                    'B19001_005E,'      #$20,000 to $24,999
                    'B19001_006E,'      #$25,000 to $29,999
                    'B19001_007E,'      #$30,000 to $34,999
                    'B19001_008E,'      #$35,000 to $39,999
                    'B19001_009E,'      #$40,000 to $44,999
                    'B19001_010E,'      #$45,000 to $49,999
                    'B19001_011E,'      #$50,000 to $59,999
                    'B19001_012E,'      #60,000 to $74,999
                    'B19001_013E,'      #$75,000 to $99,999
                    'B19001_014E,'      #$100,000 to $124,999
                    'B19001_015E,'      #$125,000 to $149,999
                    'B19001_016E,'      #$150,000 to $199,999
                    'B19001_017E'       #$200,000 or more
                    ]

#results[323:334]
earnings_type = ['B19051_001E,'     #Total Earnings Type
                 'B19051_002E,'     #Total With Earnings
                 'B19052_002E,'     #Wage Earnings
                 'B19053_002E,'     #With Self Employment Income
                 'B19054_002E,'     #With Interest Dividends and Rental Income
                 'B19055_002E,'     #With Social Security Income
                 'B19056_002E,'     #With Supplemental Security Income (SSI)
                 'B19057_002E,'     #With public assistance income
                 'B19058_002E,'     #With cash public assistance or Food Stamps/SNAP
                 'B19059_002E,'     #With retirement income
                 'B19060_002E'     #With Other Types of Income
                 ]

#results[337:354]
family_income = ['B19101_001E,'     #Estimate!!Total
                 'B19101_002E,'     #Less than $10,000
                 'B19101_003E,'     #$10,000 to $14,999
                 'B19101_004E,'     #$15,000 to $19,999
                 'B19101_005E,'     #$20,000 to $24,999
                 'B19101_006E,'     #$25,000 to $29,999
                 'B19101_007E,'     #$30,000 to $34,999
                 'B19101_008E,'     #$35,000 to $39,999
                 'B19101_009E,'     #$40,000 to $44,999
                 'B19101_010E,'     #$45,000 to $49,999
                 'B19101_011E,'     #$50,000 to $59,999
                 'B19101_012E,'     #$60,000 to $74,999
                 'B19101_013E,'     #$75,000 to $99,999
                 'B19101_014E,'     #$100,000 to $124,999
                 'B19101_015E,'     #$125,000 to $149,999
                 'B19101_016E,'     #$150,000 to $199,999
                 'B19101_017E'      #!$200,000 or more
                 ]

#results[357:371]
language_home = ['C16001_001E,'     #Language Spoken At Home
                 'C16001_002E,'     #Speak only English
                 'C16001_003E,'     #Speak Spanish
                 'C16001_006E,'     #French, Haitian, or Cajun
                 'C16001_009E,'     #Germanic or West Germanic Language
                 'C16001_012E,'     #Russian, Polish, or other Slavic languages
                 'C16001_015E,'     #Other Indo-European languages 
                 'C16001_018E,'     #Korean
                 'C16001_021E,'     #Chinese (Mandarin + Cantonese)
                 'C16001_024E,'     #Vietnamese
                 'C16001_027E,'     #Tagalog + Filipino
                 'C16001_030E,'     #Other Asian and Pacific Island Language
                 'C16001_033E,'     #Arabic
                 'C16001_036E'     #Other Unspecified Language
                 ]

#results[374:405]
occupation_median_earnings = ['B24011_001E,'        #Estimate Total
                              'B24011_003E,'        #Management, business, and financial occupations
                              'B24011_004E,'        #Management occupations
                              'B24011_005E,'        #Business and financial operations occupations
                              'B24011_006E,'        #Computer, engineering, and science occupations
                              'B24011_007E,'        #Computer and mathematical occupations
                              'B24011_008E,'        #Architecture and engineering occupations
                              'B24011_009E,'        #Life, physical, and social science occupations
                              'B24011_010E,'        #Education, legal, community service, arts, and media occupations
                              'B24011_011E,'        #Community and social service occupations
                              'B24011_012E,'        #Legal occupations
                              'B24011_013E,'        #Education, training, and library occupations
                              'B24011_014E,'        #Arts, design, entertainment, sports, and media occupations
                              'B24011_015E,'        #Healthcare practitioners and technical occupations
                              'B24011_016E,'        #Health diagnosing and treating practitioners and other technical occupations
                              'B24011_017E,'        #Health technologists and technicians
                              'B24011_019E,'        #Healthcare support occupations
                              'B24011_020E,'        #Protective service occupations
                              'B24011_021E,'        #Fire fighting and prevention, and other protective service workers including supervisors
                              'B24011_022E,'        #Law enforcement workers including supervisors
                              'B24011_023E,'        #Food preparation and serving related occupations
                              'B24011_024E,'        #Building and grounds cleaning and maintenance occupations
                              'B24011_025E,'        #Personal care and service occupations
                              'B24011_027E,'        #Sales and related occupations
                              'B24011_028E,'        #Office and administrative support occupations
                              'B24011_030E,'        #Farming, fishing, and forestry occupations
                              'B24011_031E,'        #Construction and extraction occupations
                              'B24011_032E,'        #Installation, maintenance, and repair occupations
                              'B24011_034E,'        #Production occupations
                              'B24011_035E,'        #Transportation occupations
                              'B24011_036E'        #Material moving occupations
                              ]

#results[408:422]
occupation = ['C24050_002E,'    #Agriculture, forestry, fishing and hunting, and mining
              'C24050_003E,'    #Construction
              'C24050_004E,'    #Manufacturing
              'C24050_005E,'    #Wholesale trade
              'C24050_006E,'    #Retail trade
              'C24050_007E,'    #Transportation and warehousing, and utilities
              'C24050_008E,'    #Information
              'C24050_009E,'    #Finance and insurance, and real estate and rental and leasing
              'C24050_010E,'    #Professional, scientific, and management, and administrative and waste management services
              'C24050_011E,'    #Educational services, and health care and social assistance
              'C24050_012E,'    #Arts, entertainment, and recreation, and accommodation and food services
              'C24050_013E,'    #Other services, except public administration
              'C24050_014E,'    #Public administration
              'C24050_001E'     #Total
              ]

#results[425:427]
occupancy_status = ['B25002_002E,'      #Total Occupied
                    'B25002_003E'       #Total Vacant
                    ]

#results[430:432]
tenure_status = ['B25003_002E,'     #Owner occupied
                 'B25003_003E'     #Renter occupied
                 ]

#results[435:443]
vacancy_status = ['B25004_001E,'    #Total Vacancy Status
                  'B25004_002E,'    #For Rent
                  'B25004_003E,'    #Rented, Not Occupied
                  'B25004_004E,'    #For Sale Only
                  'B25004_005E,'    #Sold, not occupied
                  'B25004_006E,'    #For seasonal, recreational, or occasional use
                  'B25004_007E,'    #For migrant workers
                  'B25004_008E'     #Other vacant
                  ]

#results[446:467]
householder_age = ['B25007_001E,'       #Total occupied
                   'B25007_002E,'       #Owner occupied
                   'B25007_003E,'       #Owner occupied!!Householder 15 to 24 years
                   'B25007_004E,'       #Owner occupied!!Householder 25 to 34 years
                   'B25007_005E,'       #Owner occupied!!Householder 35 to 44 years
                   'B25007_006E,'       #Owner occupied!!Householder 45 to 54 years
                   'B25007_007E,'       #Owner occupied!!Householder 55 to 59 years
                   'B25007_008E,'       #Owner occupied!!Householder 60 to 64 years
                   'B25007_009E,'       #Owner occupied!!Householder 65 to 74 years
                   'B25007_010E,'       #Owner occupied!!Householder 75 to 84 years
                   'B25007_011E,'       #Owner occupied!!Householder 85 years and over
                   'B25007_012E,'       #Renter occupied
                   'B25007_013E,'       #Renter occupied!!Householder 15 to 24 years
                   'B25007_014E,'       #Renter occupied!!Householder 25 to 34 years
                   'B25007_015E,'       #Renter occupied!!Householder 35 to 44 years
                   'B25007_016E,'       #Renter occupied!!Householder 45 to 54 years
                   'B25007_017E,'       #Renter occupied!!Householder 55 to 59 years
                   'B25007_018E,'       #Renter occupied!!Householder 60 to 64 years
                   'B25007_019E,'       #Renter occupied!!Householder 65 to 74 years
                   'B25007_020E,'       #Renter occupied!!Householder 75 to 84 years
                   'B25007_021E'       #Renter occupied!!Householder 85 years and over
                             ]

#results[470:487]
household_size = ['B25009_001E,'    #Total
                  'B25009_002E,'    #Total Owner Occupied
                  'B25009_003E,'    #Owner Occupied, 1 Person Household
                  'B25009_004E,'    #Owner occupied, 2-person household
                  'B25009_005E,'    #Owner occupied, 3-person household
                  'B25009_006E,'    #Owner occupied!!4-person household
                  'B25009_007E,'    #Owner occupied!!5-person household
                  'B25009_008E,'    #Owner occupied!!6-person household
                  'B25009_009E,'    #Owner occupied!!7-or-more person household
                  'B25009_010E,'    #Renter occupied
                  'B25009_011E,'    #Renter occupied!!1-person household
                  'B25009_012E,'    #Renter occupied!!2-person household
                  'B25009_013E,'    #Renter occupied!!3-person household
                  'B25009_014E,'    #Renter occupied!!4-person household
                  'B25009_015E,'    #Renter occupied!!5-person household
                  'B25009_016E,'    #Renter occupied!!6-person household
                  'B25009_017E'    #Renter occupied!!7-or-more person household
                  ]

#results[490:520]
contract_rent = ['B25056_001E,'     #Total
                 'B25056_002E,'     #With Cash Rent
                 'B25056_027E,'     #No Cash Rent
                 'B25056_003E,'     #With cash rent!!Less than $100
                 'B25056_004E,'     #With cash rent!!$100 to $149
                 'B25056_005E,'     #With cash rent!!$150 to $199
                 'B25056_006E,'     #With cash rent!!$200 to $249
                 'B25056_007E,'     #With cash rent!!$250 to $299
                 'B25056_008E,'     #With cash rent!!$300 to $349
                 'B25056_009E,'     #With cash rent!!$350 to $399
                 'B25056_010E,'     #With cash rent!!$400 to $449
                 'B25056_011E,'     #With cash rent!!$450 to $499
                 'B25056_012E,'     #With cash rent!!$500 to $549
                 'B25056_013E,'     #With cash rent!!$550 to $599
                 'B25056_014E,'     #With cash rent!!$600 to $649
                 'B25056_015E,'     #With cash rent!!$650 to $699
                 'B25056_016E,'     #With cash rent!!$700 to $749
                 'B25056_017E,'     #With cash rent!!$750 to $799
                 'B25056_018E,'     #With cash rent!!$800 to $899
                 'B25056_019E,'     #With cash rent!!$900 to $999
                 'B25056_020E,'     #With cash rent!!$1,000 to $1,249
                 'B25056_021E,'     #With cash rent!!$1,250 to $1,499
                 'B25056_022E,'     #With cash rent!!$1,500 to $1,999
                 'B25056_023E,'     #With cash rent!!$2,000 to $2,499
                 'B25056_024E,'     #With cash rent!!$2,500 to $2,999
                 'B25056_025E,'     #With cash rent!!$3,000 to $3,499
                 'B25056_026E,'     #With cash rent!!$3,500 or more
                 'B25057_001E,'     #Lower contract rent quartile
                 'B25058_001E,'     #Median contract rent
                 'B25059_001E'     #Upper contract rent quartile
                 ]

#results[523:548]
rent_asked = ['B25061_001E,'    #Total
              'B25061_002E,'    #Less than $100
              'B25061_003E,'    #$100 to $149
              'B25061_004E,'    #$150 to $199
              'B25061_005E,'    #$200 to $249
              'B25061_006E,'    #$250 to $299
              'B25061_007E,'    #$300 to $349
              'B25061_008E,'    #$350 to $399
              'B25061_009E,'    #$400 to $449
              'B25061_010E,'    #$450 to $499
              'B25061_011E,'    #$500 to $549
              'B25061_012E,'    #$550 to $599
              'B25061_013E,'    #$600 to $649
              'B25061_014E,'    #$650 to $699
              'B25061_015E,'    #$700 to $749
              'B25061_016E,'    #$750 to $799
              'B25061_017E,'    #$800 to $899
              'B25061_018E,'    #$900 to $999
              'B25061_019E,'    #$1,000 to $1,249
              'B25061_020E,'    #$1,250 to $1,499
              'B25061_021E,'    #$1,500 to $1,999
              'B25061_022E,'    #2,000 to $2,499
              'B25061_023E,'    #$2,500 to $2,999
              'B25061_024E,'    #$3,000 to $3,499
              'B25061_025E'    #$3,500 or more
              ]

#results[551:580]
house_value = ['B25075_002E,'   #Less than $10,000
               'B25075_003E,'   #$10,000 to $14,999
               'B25075_004E,'   #$15,000 to $19,999
               'B25075_005E,'   #$20,000 to $24,999
               'B25075_006E,'   #$25,000 to $29,999
               'B25075_007E,'   #$30,000 to $34,999
               'B25075_008E,'   #$35,000 to $39,999
               'B25075_009E,'   #$40,000 to $49,999
               'B25075_010E,'   #$50,000 to $59,999
               'B25075_011E,'   #$60,000 to $69,999
               'B25075_012E,'   #$70,000 to $79,999
               'B25075_013E,'   #$80,000 to $89,999
               'B25075_014E,'   #$90,000 to $99,999
               'B25075_015E,'   #$100,000 to $124,999
               'B25075_016E,'   #$125,000 to $149,999
               'B25075_017E,'   #$150,000 to $174,999
               'B25075_018E,'   #$175,000 to $199,999
               'B25075_019E,'   #$200,000 to $249,999
               'B25075_020E,'   #$250,000 to $299,999
               'B25075_021E,'   #$300,000 to $399,999
               'B25075_022E,'   #$400,000 to $499,999
               'B25075_023E,'   #$500,000 to $749,999
               'B25075_024E,'   #$750,000 to $999,999
               'B25075_025E,'   #$1,000,000 to $1,499,999
               'B25075_026E,'   #$1,500,000 to $1,999,999
               'B25075_027E,'   #$2,000,000 or more
               'B25076_001E,'   #lower value quartile (dollars)
               'B25077_001E,'   #Median value (dollars)
               'B25078_001E'   #Upper value quartile (dollars)
               ]

#results[583:609]
price_asked = ['B25085_002E,'   #Less than $10,000
               'B25085_003E,'   #$10,000 to $14,999
               'B25085_004E,'   #$15,000 to $19,999
               'B25085_005E,'   #$20,000 to $24,999
               'B25085_006E,'   #$25,000 to $29,999
               'B25085_007E,'   #$30,000 to $34,999
               'B25085_008E,'   #$35,000 to $39,999
               'B25085_009E,'   #$40,000 to $49,999
               'B25085_010E,'   #$50,000 to $59,999
               'B25085_011E,'   #$60,000 to $69,999
               'B25085_012E,'   #$70,000 to $79,999
               'B25085_013E,'   #$80,000 to $89,999
               'B25085_014E,'   #$90,000 to $99,999
               'B25085_015E,'   #$100,000 to $124,999
               'B25085_016E,'   #$125,000 to $149,999
               'B25085_017E,'   #$150,000 to $174,999
               'B25085_018E,'   #$175,000 to $199,999
               'B25085_019E,'   #$200,000 to $249,999
               'B25085_020E,'   #$250,000 to $299,999
               'B25085_021E,'   #$300,000 to $399,999
               'B25085_022E,'   #$400,000 to $499,999
               'B25085_023E,'   #$500,000 to $749,999
               'B25085_024E,'   #$750,000 to $999,999
               'B25085_025E,'   #$1,000,000 to $1,499,999
               'B25085_026E,'   #$1,500,000 to $1,999,999
               'B25085_027E'   #$2,000,000 or more
               ]

#results[612:620]
mortgage_status = ['B25081_001E,'   #Total Mortgage Status
                   'B25081_002E,'   #Housing units with a mortgage, contract to purchase, or similar debt
                   'B25081_003E,'   #With either a second mortgage or home equity loan, but not both
                   'B25081_004E,'   #Second mortgage only
                   'B25081_005E,'   #Home equity loan only
                   'B25081_006E,'   #Both second mortgage and home equity loan
                   'B25081_007E,'   #No second mortgage and no home equity loan
                   'B25081_008E'    #Housing units without a mortgage
                   ]

#results[623:641]
monthly_owner_costs = ['B25094_001E,'   #selected monthly costs
                       'B25094_002E,'   #Less than $200
                       'B25094_003E,'   #$200 to $299
                       'B25094_004E,'   #$300 to $399
                       'B25094_005E,'   #$400 to $499
                       'B25094_006E,'   #$500 to $599
                       'B25094_007E,'   #$600 to $699
                       'B25094_008E,'   #$700 to $799
                       'B25094_009E,'   #$800 to $899
                       'B25094_010E,'   #$900 to $999
                       'B25094_011E,'   #$1,000 to $1,249
                       'B25094_012E,'   #$1,250 to $1,499
                       'B25094_013E,'   #$1,500 to $1,999
                       'B25094_014E,'   #$2,000 to $2,499
                       'B25094_015E,'   #$2,500 to $2,999
                       'B25094_016E,'   #$3,000 to $3,499
                       'B25094_017E,'   #$3,500 to $3,999
                       'B25094_018E'    #$4,000 or more
                           ]

#results[644:662]
total_housing_costs = ['B25104_001E,'   #Estimate!!Total
                       'B25104_002E,'   #Less than $100
                       'B25104_003E,'   #$100 to $199
                       'B25104_004E,'   #$200 to $299
                       'B25104_005E,'   #$300 to $399
                       'B25104_006E,'   #$400 to $499
                       'B25104_007E,'   #$500 to $599
                       'B25104_008E,'   #$600 to $699
                       'B25104_009E,'   #$700 to $799
                       'B25104_010E,'   #$800 to $899
                       'B25104_011E,'   #$900 to $999
                       'B25104_012E,'   #$1,000 to $1,499
                       'B25104_013E,'   #$1,500 to $1,999
                       'B25104_014E,'   #$2,000 to $2,499
                       'B25104_015E,'   #$2,500 to $2,999
                       'B25104_016E,'   #$3,000 or more
                       'B25104_017E,'   #No cash rent
                       'B25105_001E'   #Median monthly housing costs
                       ]

#results[665:682]
taxes_paid = ['B25102_002E,'    #Total With A Mortgage
              'B25102_003E,'    #With a mortgage, Less than $800
              'B25102_004E,'    #With a mortgage, $800 to $1,499
              'B25102_005E,'    #With a mortgage, $1,500 to $1,999
              'B25102_006E,'    #With a mortgage, $2,000 to $2,999
              'B25102_007E,'    #With a mortgage, $3,000 or more
              'B25102_008E,'    #With a mortgage, No real estate taxes paid
              'B25102_009E,'    #Not mortgaged
              'B25102_010E,'    #Not mortgaged, Less than $800
              'B25102_011E,'    #Not mortgaged!!$800 to $1,499
              'B25102_012E,'    #Not mortgaged!!$1,500 to $1,999
              'B25102_013E,'    #Not mortgaged!!$2,000 to $2,999
              'B25102_014E,'    #Not mortgaged!!$3,000 or more
              'B25102_015E,'    #No real estate taxes paid
              'B25103_001E,'    #Median real estate taxes paid!!Total
              'B25103_002E,'    #Median real estate taxes paid for units with a mortgage
              'B25103_003E'    #Median real estate taxes paid for units without a mortgage
              ]

#results[685:692]
bedrooms = ['B25041_001E,'      #Bedrooms Total
            'B25041_002E,'      #No bedroom
            'B25041_003E,'      #1 bedroom
            'B25041_004E,'      #2 bedrooms
            'B25041_005E,'      #3 bedrooms
            'B25041_006E,'      #4 bedrooms
            'B25041_007E'      #5 or more bedrooms
            ]

#results[695:706]
year_structure_built = ['B25034_002E,'      #Built 2014 or later
                        'B25034_003E,'      #Built 2010 to 2013
                        'B25034_004E,'      #Built 2000 to 2009
                        'B25034_005E,'      #Built 1990 to 1999
                        'B25034_006E,'      #Built 1980 to 1989
                        'B25034_007E,'      #Built 1970 to 1979
                        'B25034_008E,'      #Built 1960 to 1969
                        'B25034_009E,'      #Built 1950 to 1959
                        'B25034_010E,'      #Built 1940 to 1949
                        'B25034_011E,'      #Built 1939 or earlier
                        'B25035_001E'      #Median year structure built
                        ]

#results[709:732]
units_in_structure = ['B25032_001E,'        #Total Units in Structure
                      'B25032_002E,'        #Owner-occupied housing units
                      'B25032_003E,'        #Owner-occupied housing units!!1, detached
                      'B25032_004E,'        #Owner-occupied housing units!!1, attached
                      'B25032_005E,'        #Owner-occupied housing units!!2
                      'B25032_006E,'        #Owner-occupied housing units!!3 or 4
                      'B25032_007E,'        #Owner-occupied housing units!!5 to 9
                      'B25032_008E,'        #Owner-occupied housing units!!10 to 19
                      'B25032_009E,'        #Owner-occupied housing units!!20 to 49
                      'B25032_010E,'        #Owner-occupied housing units!!50 or more
                      'B25032_011E,'        #Owner-occupied housing units!!Mobile home
                      'B25032_012E,'        #Owner-occupied housing units!!Boat, RV, van, etc.
                      'B25032_013E,'        #Renter-occupied housing units
                      'B25032_014E,'        #Renter-occupied housing units!!1, detached
                      'B25032_015E,'        #Renter-occupied housing units!!1, attached
                      'B25032_016E,'        #Renter-occupied housing units!!2
                      'B25032_017E,'        #Renter-occupied housing units!!3 or 4
                      'B25032_018E,'        #Renter-occupied housing units!!5 to 9
                      'B25032_019E,'        #Renter-occupied housing units!!10 to 19
                      'B25032_020E,'        #Renter-occupied housing units!!20 to 49
                      'B25032_021E,'        #Renter-occupied housing units!!50 or more
                      'B25032_022E,'        #!Renter-occupied housing units!!Mobile home
                      'B25032_023E'        #Renter-occupied housing units!!Boat, RV, van, etc.
                      ]

#results[735:785]
other_race1 = ['B02017_002E,'  #American Indian Ancestry
               'B02017_046E,'  #Alaskan Native Ancestry
               'B02018_002E,'  # Asian Indian
               'B02018_003E,'  # Bangladeshi
               'B02018_004E,'  # Bhutanese
               'B02018_005E,'  # Burmese
               'B02018_006E,'  # Cambodian
               'B02018_007E,'  # Chinese, except Taiwanese
               'B02018_008E,'  # Filipino
               'B02018_009E,'  # Hmong
               'B02018_010E,'  # Indonesian
               'B02018_011E,'  # Japanese
               'B02018_012E,'  # Korean
               'B02018_013E,'  # Laotian
               'B02018_014E,'  # Malaysian
               'B02018_015E,'  # Mongolian
               'B02018_016E,'  # Nepalese
               'B02018_017E,'  # Okinawan
               'B02018_018E,'  # Pakistani
               'B02018_019E,'  # Sri Lankan
               'B02018_020E,'  # Taiwanese
               'B02018_021E,'  # Thai
               'B02018_022E,'  # Vietnamese
               'B02018_023E,'  # Other Asian Specified
               'B02018_024E,'  # Other Asian, not specified
               'B02019_002E,'  # Native Hawaiian
               'B02019_003E,'  # Samoan
               'B02019_004E,'  # Tongan
               'B02019_005E,'  # Other Polynesian
               'B02019_006E,'  # Guamanian or Chamorro
               'B02019_007E,'  # Marshallese
               'B02019_008E,'  # Other Micronesian
               'B02019_009E,'  # Fijian
               'B02019_010E,'  # Other Melanesian
               'B03001_004E,'  # Mexican
               'B03001_005E,'  # Puerto Rican
               'B03001_006E,'  # Cuban
               'B03001_007E,'  # Dominican (Dominican Republic)
               'B03001_009E,'  # Costa Rican
               'B03001_010E,'  # Guatemalan
               'B03001_011E,'  # Honduran
               'B03001_012E,'  # Nicaraguan
               'B03001_013E,'  # Panamanian
               'B03001_014E,'  # Salvadoran
               'B03001_015E,'  # Other Central American
               'B03001_017E,'  # Argentinean
               'B03001_018E,'  # Bolivian
               'B03001_019E,'  # Chilean
               'B03001_020E,'  # Colombian
               'B03001_021E'  # Ecuadorian
               ]

#results[788:797]
other_race2 = ['B03001_022E,'   #Paraguayan
               'B03001_023E,'   #Peruvian
               'B03001_024E,'   #Uruguayan
               'B03001_025E,'   #Venezuelan
               'B03001_026E,'   #Other South American
               'B03001_027E,'   #Other Hispanic or Latino
               'B03001_029E,'   #Spanish
               'B03001_028E,'   #Spaniard
               'B03001_030E'    #Spanish American
               ]



#----------------------------------------------------------------------------------------------------


#ACS 2016 Community Survey - Detailed Tables

web_scrape_url = ['https://api.census.gov/data/2016/acs/acs5?']


#this list is the combined results of all the 50 item api calls
results = []


#this part of the code requires different census calls to get information
list = [summary, demographics, race, ethnicity1, ethnicity2, foreign_native, relationship, education,
        transportation, work, travel_time, vehicles, worker_class, under18,
        school_enrollment, bachelors_field_study, nativity_language, household_income_past_12,
        earnings_type, family_income, language_home, occupation_median_earnings, occupation,
        occupancy_status, tenure_status, vacancy_status, householder_age, household_size, contract_rent, rent_asked,
        house_value, price_asked, mortgage_status, monthly_owner_costs, total_housing_costs, taxes_paid,
        bedrooms, year_structure_built, units_in_structure, other_race1, other_race2]



for x in list:
    #census tract level
    censusparams1 = {
        'get': x,
        'for': 'tract:' + tract_id,
        'in': 'state:' + state_id + ' county:' + county_id,
        'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }

    #census block level
    censusparams2 = {
        'get': x,
        'for': 'block group:' + block_group,
        'in': 'state:' + state_id + ' county:' + county_id + ' tract:' + tract_id,
        'key':'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }

    #zipcode level
    censusparams3 = {
        'get': x,
        'for': 'zip code tabulation area:' + zipcode,
        'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'

    }
    #public use microdata area
    censusparams4 = {
        'get': x,
        'for': 'public use microdata area:' + microdata_id,
        'in': 'state:' + state_id,
        'key': 'ec7ebde81a7a1772203e43dfed95a061d4c5118d'
    }

    # metropolitan statistical area
    censusparams5 = {
        'get': x,
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
    req = requests.get('https://api.census.gov/data/2016/acs/acs5?', params=parameter)
    res = req.json()
    preresults = res[1]
    #preresults as a result of for-loops to acquire data
    print(preresults)
    #taking the presults and appending to results
    for y in preresults:
        results.append(y)

print(results[735:785])
#----------------------------------[CREATING PANDA DATAFRAMES]--------------------------------------------------



male_age_distribution_values = results[20:43]
male_age_distribution_keys = ["Under 5 years",
                              "5 to 9 years",
                              "10 to 14 years",
                              "15 to 17 years",
                              "18 and 19 years",
                              "20 years",
                              "21 years",
                              "22 to 24 years",
                              "25 to 29 years",
                              "30 to 34 years",
                              "35 to 39 years",
                              "40 to 44 years",
                              "45 to 49 years",
                              "50 to 54 years",
                              "55 to 59 years",
                              "60 and 61 years",
                              "62 to 64 years",
                              "65 and 66 years",
                              "67 to 69 years",
                              "70 to 74 years",
                              "75 to 79 years",
                              "80 to 84 years",
                              "85 years and over"
                              ]

#
male_age_distribution = dict(zip(male_age_distribution_keys, male_age_distribution_values))
#convert to pandas data series
MALE_AGE_DISTRIBUTION = pd.Series(male_age_distribution)


#----------------------------------[PANDA SERIES]-----------------------------------------------------

female_age_distribution_keys = ["Under 5 years",
                              "5 to 9 years",
                              "10 to 14 years",
                              "15 to 17 years",
                              "18 and 19 years",
                              "20 years",
                              "21 years",
                              "22 to 24 years",
                              "25 to 29 years",
                              "30 to 34 years",
                              "35 to 39 years",
                              "40 to 44 years",
                              "45 to 49 years",
                              "50 to 54 years",
                              "55 to 59 years",
                              "60 and 61 years",
                              "62 to 64 years",
                              "65 and 66 years",
                              "67 to 69 years",
                              "70 to 74 years",
                              "75 to 79 years",
                              "80 to 84 years",
                              "85 years and over"
                              ]

female_age_distribution_values = results[44:67]

#create python dictionary
female_age_distribution = dict(zip(female_age_distribution_keys, female_age_distribution_values))

#convert to pandas data series
FEMALE_AGE_DISTRIBUTION = pd.Series(female_age_distribution)


#-----------------------------------------------------------------------------------------------------


#Total Age Distribution

dfnew = pd.to_numeric(MALE_AGE_DISTRIBUTION, errors='raise', downcast=None)
df2new = pd.to_numeric(FEMALE_AGE_DISTRIBUTION, errors='raise', downcast=None)

TOTAL_AGE_DISTRIBUTION = dfnew.add(df2new)

print(TOTAL_AGE_DISTRIBUTION)
#---------------------------------------------------------------------------------------------------------


race_values = results[70:78]
race_keys = ['White',
             'Hispanic',
             'Black',
             'Asian',
             'Native American/Alaskan Native',
             'Native Hawaiian/Pacific Islander',
             'Other',
             'Two or More Races'
             ]
race = dict(zip(race_keys, race_values))
RACE = pd.Series(race)

print(RACE)


#---------------------------------------------------------------------------------------------------------


ethnicity1_values = results[82:123]
ethnicity2_values = results[126:156]

ethnicity_values = ethnicity1_values + ethnicity2_values

print(ethnicity_values)





























#labels = ['Men', 'Women']
#values = [results[25], results[1]]

#trace = go.Pie(labels=labels, values=values)

#py.iplot([trace], filename='basic_pie_chart')

#-------------------------------------------[plot online]-----------------------------------------------------------------------------------------

#MALE_AGE_DISTRIBUTION.iplot(kind='bar', yTitle='Male Age Distribution', title="Male Age Distribution")
#FEMALE_AGE_DISTRIBUTION.iplot(kind='bar', yTitle='Female Age Distribution', title="Female Age Distribution")
#TOTAL_AGE_DISTRIBUTION.iplot(kind='bar', yTitle='Total Age Distribution', title="Total Age Distribution")