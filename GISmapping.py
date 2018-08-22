import csv
from shapely.geometry import Point, mapping
from fiona import collection
import geopandas as gp
import matplotlib.pyplot as plt
import matplotlib



with open("C:/Users/Joe/Documents/42Floors/2018-08-08_23_12_24/Houston()/houstonproperties_08_14_2018.csv", 'r', encoding='ISO-8859-1') as  f:
    reader = csv.DictReader(f)

# write latitude longitude in csv into shapefile, with properties
schema = {'geometry': 'Point',
          'properties': {'address': 'str',
                         'city': 'str',
                         'state': 'str',
                         'zipcode': 'str',
                         'walkability': 'str',
                         'walkabilitydescription': 'str',
                         'bikability': 'str',
                         'bikabilitydescription': 'str',
                         },

          }
with collection("Houston.shp", "w", "ESRI Shapefile", schema) as output:
    with open('C:/Users/Joe/Documents/42Floors/2018-08-08_23_12_24/Houston()/houstonproperties_08_14_2018.csv', 'r',
              encoding='ISO-8859-1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            point = Point(float(row['lon']), float(row['lat']))
            output.write({
                'properties': {
                    'address': row['address'],
                    'city': row['city'],
                    'state': row['state'],
                    'zipcode': row['zipcode'],
                    'walkability': row['walkability'],
                    'walkabilitydescription': row['walkabilitydescription'],
                    'bikability': row['bikability'],
                    'bikabilitydescription': row['bikabilitydescription'],
                },  # add all the properties into the shapefile point!
                'geometry': mapping(point)
            })


realestatelocations = gp.GeoDataFrame.from_file(
    'C:/Users/Joe/PycharmProjects/GIS/Houston.shp')

states = gp.read_file("C:/Users/Joe/Downloads/gz_2010_48_140_00_500k/gz_2010_48_140_00_500k.shp")

# Get current size

fig_size = plt.rcParams["figure.figsize"]

# Prints: [8.0, 6.0]
print("Current size:", fig_size)

# Set figure width to 12 and height to 9
fig_size[0] = 24
fig_size[1] = 18
plt.rcParams["figure.figsize"] = fig_size

ax = states.plot(linewidth=0.25, edgecolor='white', color='lightgrey')
map = realestatelocations.plot(column='walkabilit', alpha=0.3, ax=ax)


matplotlib.pyplot.show(map)





