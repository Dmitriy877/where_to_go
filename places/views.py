from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Place
from django.urls import reverse


def start_page(request):

    all_places = Place.objects.all()
    places_for_index = []

    for place in all_places:

        place_for_index = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.coordinates_lng, place.coordinates_lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': reverse(place_page, args=[place.id])
            }
        }

        places_for_index.append(place_for_index)

    places = {
      'type': 'FeatureCollection',
      'features': places_for_index
    }
    context = {'places_json': places}
    return render(request, 'index.html', context)


def place_page(request, id: int):

    place = get_object_or_404(Place, pk=id)

    pictures = place.pictures.all()
    pictures_urls = [
        picture.picture.url for picture in pictures
    ]

    json_place = {
        'title': place.title,
        'imgs': pictures_urls,
        'description_short': place.short_description,
        'description_long': place.long_description,
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
