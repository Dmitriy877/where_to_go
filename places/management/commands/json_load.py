from django.core.management.base import BaseCommand
from places.models import Place, PlacePicture
from django.core.files.base import ContentFile
import requests
from requests.exceptions import HTTPError, ConnectionError
import time


class Command(BaseCommand):
    help = 'Укажите путь до json файла как аргумент'

    def add_arguments(self, parser):
        parser.add_argument(
            'load_picture_from_json',
            type=str,
            help='Укажите путь до json файла как аргумент'
        )

    def handle(self, *args, **options):
        try:
            response = requests.get(options['load_picture_from_json'])
            response.raise_for_status()
            payload = response.json()
        except Exception:
            print('Ошибка при загрузке файла')

        try:
            place_location, created = Place.objects.get_or_create(
                title=payload['title'],
                short_description=payload['description_short'],
                long_description=payload['description_long'],
                coordinates_lng=payload['coordinates']['lng'],
                coordinates_lat=payload['coordinates']['lat'],
            )
        except Exception:
            print('Указанная локация уже добавлена')

        image_urls = payload['imgs']

        for index, image_url in enumerate(image_urls, start=1):
            step = 0
            while step <= len(image_urls):
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()
                    content = ContentFile(
                        response.content,
                        name=f'{place_location}{index}'
                    )
                    picture, created = PlacePicture.objects.get_or_create(
                        number=index,
                        place=place_location,
                        picture=content,
                    )
                    step += 1
                except HTTPError:
                    print(f'Ошибка загрузки изображения по адресу {image_url}. Проверьте правильность указания ссылок')
                    continue
                except ConnectionError:
                    print('Ошибка соединения. Попытка установить соединение')
                    time.sleep(10)
                    continue
