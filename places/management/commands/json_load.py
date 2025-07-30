from django.core.management.base import BaseCommand
from places.models import Place, PlacePicture
from django.core.files.base import ContentFile
import requests


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
            if not response.status_code == requests.codes.ok:
                raise Exception
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
            response = requests.get(image_url)
            content = ContentFile(response.content)
            picture, created = PlacePicture.objects.get_or_create(
                number=index,
                place=place_location,
            )
            picture.picture.save(
                f'{place_location}{index}',
                content, save=True
            )
