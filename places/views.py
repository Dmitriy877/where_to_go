from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Place
from django.urls import reverse


def start_page(request):

    places = Place.objects.all()
    places_for_index = []

    for place in places:

        place_for_index = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.coordinates_lng, place.coordinates_lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.place_id,
                'detailsUrl': reverse(place_page, args=[place.id])
            }
        }

        places_for_index.append(place_for_index)

    places_json = {
      'type': 'FeatureCollection',
      'features': places_for_index
    }

    template = loader.get_template('index.html')
    context = {'places_json': places_json}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def place_page(request, id: int):

    place = get_object_or_404(Place, pk=id)

    pictures = place.pictures.all()
    pictures_urls = [
        picture.picture.url for picture in pictures
    ]

    json_place = {
        'title': place.title,
        'imgs': pictures_urls,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.coordinates_lng,
            'lat': place.coordinates_lat
        }
    }

    response = JsonResponse(json_place, json_dumps_params={
                                        'indent': 2,
                                        'ensure_ascii': False,
                                     })

    return response
