from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='Наименование',
    )
    short_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Короткое описание',
    )
    long_description = HTMLField(
        null=True,
        blank=True,
        verbose_name='Длинное описание',
    )
    coordinates_lng = models.FloatField(
        verbose_name='Координаты долготы'
    )
    coordinates_lat = models.FloatField(
        verbose_name='Координаты широты',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.title


class PlacePicture(models.Model):
    number = models.IntegerField(
        db_index=True,
        null=True,
        blank=True,
        default=None,
    )
    place = models.ForeignKey(
        Place,
        verbose_name='Локация',
        on_delete=models.CASCADE,
        related_name='pictures'
    )
    picture = models.ImageField(
        upload_to='place_pictures/',
        verbose_name='Загруженная фотография',
    )

    class Meta:
        ordering = ['number']
        verbose_name = 'Загруженные фотографии'

    def __str__(self):
        return f'{self.number} {self.place}'
