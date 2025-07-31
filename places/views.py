from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from .models import Place


def start_page(request):

    places = Place.objects.all()
    places_list = []

    for place in places:

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

        places_list.append(place_for_index)

    places_dict = {
      'type': 'FeatureCollection',
      'features': places_list
    }
    context = {'places_json': places_dict}
    return render(request, 'index.html', context)


def place_page(request, id: int):

    place = get_object_or_404(Place.objects.prefetch_related('pictures'), pk=id)
    pictures = place.pictures.all()
    pictures_urls = [
        picture.picture.url for picture in pictures
    ]

    serialized_place = {
        'title': place.title,
        'imgs': pictures_urls,
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lng': place.coordinates_lng,
            'lat': place.coordinates_lat
        }
    }

    response = JsonResponse(serialized_place, json_dumps_params={
                                        'indent': 2,
                                        'ensure_ascii': False,
                                     })

    return response
