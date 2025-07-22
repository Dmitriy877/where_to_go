from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Place
import os
import pprint


def start_page(request):
    places = Place.objects.all()
    places_for_index = []
    for place in places:
        pictures = place.pictures.all()
        pictures_list = [picture.picture.url for picture in pictures]

        details_url = {
            "title": place.title,
            "imgs": pictures_list,
            "description_short": place.description_short,
            "description_long": place.description_long,
            "coordinates": {
                "lng": place.coordinates_lng,
                "lat": place.coordinates_lat
            }
        }

        if place.title == 'Экскурсионная компания «Легенды Москвы»':
            path = os.path.join('static', 'places', 'moscow_legends.json')
        else:
            path = os.path.join('static', 'places', 'roofs24.json')

        place_for_index = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.coordinates_lng, place.coordinates_lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.place_id,
                "detailsUrl": path
            }
        }

        places_for_index.append(place_for_index)

    places_json = {
      "type": "FeatureCollection",
      "features": places_for_index
    }

    template = loader.get_template('index.html')
    context = {'places_json': places_json}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


# # Create your views here.
# <script id="places-geojson" type="application/json">
#   {
#     "type": "FeatureCollection",
#     "features": [
#       {
#         "type": "Feature",
#         "geometry": {
#           "type": "Point",
#           "coordinates": [37.62, 55.793676]
#         },
#         "properties": {
#           "title": "«Легенды Москвы",
#           "placeId": "moscow_legends",
#           "detailsUrl": "{% static "./places/moscow_legends.json" %}"
#         }
#       },
#       {
#         "type": "Feature",
#         "geometry": {
#           "type": "Point",
#           "coordinates": [37.64, 55.753676]
#         },
#         "properties": {
#           "title": "Крыши24.рф",
#           "placeId": "roofs24",
#           "detailsUrl": "{% static "./places/roofs24.json" %}"
#         }
#       }
#     ]
#   }
# </script>