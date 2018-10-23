from googleplaces import GooglePlaces, types, lang


YOUR_API_KEY = 'AIzaSyAEEIuRKOBNzOjMADj4hE5bGUdAFKz9oDE'

google_places = GooglePlaces(YOUR_API_KEY)

query_result = google_places.nearby_search(
        location='1 Seaport Ln, Boston, MA 02210',
        radius=10, types=[types.TYPE_POINT_OF_INTEREST])

if query_result.has_attributions:
    print (query_result.html_attributions)

for place in query_result.places:
    # Returned places from a query are place summaries.
    print(place.name)
    print(place.geo_location)
    print(place.place_id)

for photo in place.photos:
    # 'maxheight' or 'maxwidth' is required
    photo.get(maxheight=500, maxwidth=500)
    # MIME-type, e.g. 'image/jpeg'
    print(photo.mimetype)
    # Image URL
    print(photo.url)
    # Original filename (optional)
    print(photo.filename)
    # Raw image data
    print(photo.data)