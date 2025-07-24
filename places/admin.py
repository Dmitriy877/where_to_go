from django.contrib import admin
from places.models import Place, Place_picture


class Place_pictureInLine(admin.TabularInline):
    model = Place_picture


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        Place_pictureInLine
    ]


admin.site.register(Place_picture)
# Register your models here.
