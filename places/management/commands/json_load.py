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
            json_data = response.json()
        except Exception:
            print('Ошибка при загрузке файла')

        try:
            place_location, created = Place.objects.get_or_create(
                title=json_data['title'],
                short_description=json_data['description_short'],
                long_description=json_data['description_long'],
                coordinates_lng=json_data['coordinates']['lng'],
                coordinates_lat=json_data['coordinates']['lat'],
            )
        except Exception:
            print('Указанная локация уже добавлена')

        image_urls = json_data['imgs']
        for index, image_url in enumerate(image_urls):
            number = index+1
            response = requests.get(image_url)
            content = ContentFile(response.content)
            picture, created = PlacePicture.objects.get_or_create(
                number=number,
                place=place_location,
            )
            picture.picture.save(
                f'{place_location}{number}',
                content, save=True
            )
