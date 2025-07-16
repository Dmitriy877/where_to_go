from django.db import models

# Create your models here


class Place(models.Model):
    title = models.CharField(
        'Наименование',
        max_length=50,
    )
    description_short = models.TextField(
        'Короткое описание',
        max_length=300,
    )
    description_long = models.TextField(
        'Длинное описание',
    )
    coordinates_lng = models.FloatField(
        'Координаты долготы',
    )
    coordinates_lat = models.FloatField(
        'Координаты широты',
    )

    def __str__(self):
        return f'{self.title}'
