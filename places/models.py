from django.db import models

# Create your models here


class Place(models.Model):
    title = models.CharField(
        'Наименование',
        max_length=50,
        db_index=True
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
    place_id = models.CharField(
        'place id',
        max_length=50,
    )

    class Meta:
        ordering = ['title']
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return f'{self.title}'


class Place_picture(models.Model):
    number = models.IntegerField(db_index=True)
    place = models.ForeignKey(
        Place,
        verbose_name='Локация',
        on_delete=models.CASCADE,
        related_name='pictures'
    )
    picture = models.ImageField(
        upload_to='place_pictures/',
    )

    class Meta:
        ordering = ['number']
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return f'{self.number} {self.place}'
