import overpy
import requests
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import mapping, Polygon
import fiona
import geopandas as gpd
import pyproj
import shapely.ops as ops
from shapely.geometry import shape
from shapely.ops import transform
from functools import partial


#EPSG:4326.
import geocoder
#geocoding!

street = "465 Huntington Ave"
city = "Boston"
state = "MA"
searchradius = 20


#------------------------------------------------------------------------------------------------
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
longitude = (dictionary['coordinates']['x'])
latitude = (dictionary['coordinates']['y'])
#------------------------------------------------------------------------------------------------


#coordinates of building lookup
lat = 42.339591
lon = -71.094203
#29.757319, -95.371927 (333 Clay Street Tower)
#42.339591, -71.094203 (MFA Boston


api = overpy.Overpass()
# fetch all ways and nodes
result = api.query("""[out:json]
[timeout:25]
;
(
  node
    ["building"]
    (around:%d,%s,%s);
  way
    ["building"]
    (around:%d,%s,%s);
  relation
    ["building"]
    (around:%d,%s,%s);
);
out;
>;
out skel qt;""" % (searchradius, lat, lon, searchradius, lat, lon, searchradius, lat, lon))


node_list = []
for way in result.ways:
    housenumber = way.tags.get("addr:housenumber", "n/a")
    streetname = way.tags.get("addr:street", "n/a")
    address = housenumber + " " + streetname
    print(address)
    print(way.tags.get("name", ""))
    print(way.tags.get("building", ""))
    print(way.tags.get("height", ""))
    print(way.tags.get("building:height", ""))
    buildingfloors = way.tags.get("building:levels", "")
    print(buildingfloors + " floors")
    print(way.tags.get("building:material", ""))
    print(way.tags.get("roof:material", ""))
    print(way.tags.get("roof:shape", ""))
    print(way.tags.get("amenity", ""))
    print(way.tags.get("shop", ""))
    for node in way.nodes:
            node_list.append((float(node.lon), float(node.lat)))

for relation in result.relations:
    relation_list = []
    housenumber = relation.tags.get("addr:housenumber", "n/a")
    streetname = relation.tags.get("addr:street", "n/a")
    address = housenumber + " " + streetname
    print(address)
    print(relation.tags.get("name", ""))
    print(relation.tags.get("building", ""))
    print(relation.tags.get("height", ""))
    print(relation.tags.get("building:height", ""))
    buildingfloors = relation.tags.get("building:levels", "")
    print(buildingfloors + " floors")
    print(relation.tags.get("building:material", ""))
    print(relation.tags.get("roof:material", ""))
    print(relation.tags.get("roof:shape", ""))
    print(relation.tags.get("amenity", ""))
    print(relation.tags.get("shop", ""))
    print(relation.members)

print(node_list)


# Here's an example Shapely geometry
poly = Polygon(node_list)

# Define a polygon feature geometry with one attribute
schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
    'latitude': latitude,
    'longitude': longitude,
}

#shapely convert into correct map projection and look at bounds
geom_area = ops.transform(
    partial(
        pyproj.transform,
        pyproj.Proj(init='EPSG:4326'),
        pyproj.Proj(
            proj='aea',
            lat1=poly.bounds[1],
            lat2=poly.bounds[3])),
    poly)

#calculate the square footage of building
areasqmeters = geom_area.area
areasqfeet = areasqmeters*10.764

print(areasqmeters, areasqfeet)


# Write a new Shapefile
with fiona.open('C:/Users/Joe/Desktop/my_shp.shp', 'w', 'ESRI Shapefile', schema) as c:
    ## If there are multiple geometries, put the "for" loop here
    c.write({
        'geometry': mapping(poly),
        'properties': {'id': 1},
    })


shape=gpd.read_file('C:/Users/Joe/Desktop/my_shp.shp')
print(shape)


f, ax = plt.subplots(1)
shape.plot(ax=ax,column='id',cmap=None,)
plt.show()

