import overpy

api = overpy.Overpass()



# fetch all ways and nodes
result = api.query("""
    way(42.354707, -71.056175,42.355601, -71.055665) ["building"];
    (._;>;);
    out body;
    """)



for way in result.ways:
    housenumber = way.tags.get("addr:housenumber", "")
    streetname = way.tags.get("addr:street", "")
    print(housenumber, streetname)
    print(way.tags.get("name", ""))
    print(way.tags.get("building", ""))
    print(way.tags.get("height", ""))
    print(way.tags.get("building:height", ""))
    buildingfloors = way.tags.get("building:levels", "")
    print(buildingfloors + " floors")
    print(way.tags.get("building:material", ""))
    print(way.tags.get("amenity", ""))
    print("  Nodes:")
    for node in way.nodes:
        print(node.lat, node.lon)
