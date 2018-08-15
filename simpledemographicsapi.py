import requests

base_url = 'https://www.broadbandmap.gov/broadbandmap/demographic/2014/coordinates?'
latitude = '42.456345'
longitude = '-74.9874534'
json_url = base_url + "latitude=" + latitude + "&longitude=" + longitude + "&format=json"

print(json_url)

response = requests.get(json_url)

data = response.json()
print(type(data))
print(data['Results'])

income_below_poverty = (data['Results']['incomeBelowPoverty'])
median_income = (data['Results']['medianIncome'])
income_less_25 = (data['Results']['incomeLessThan25'])
income_between_25_and_50 = (data['Results']['incomeBetween25to50'])
income_between_50_and_100 = (data['Results']['incomeBetween50to100'])
income_between_100_and_200 = (data['Results']['incomeBetween100to200'])
income_greater_200 = (data['Results']['incomeGreater200'])
highschool_graduation_rate = (data['Results']['educationHighSchoolGraduate'])
college_education_rate = (data['Results']['educationBachelorOrGreater'])
