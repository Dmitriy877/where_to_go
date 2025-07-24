from django.contrib import admin
from places.models import Place, Place_picture
from django.utils.html import format_html


class Place_pictureInLine(admin.TabularInline):
    model = Place_picture
    readonly_fields = [
            'get_picture_image',
        ]

    def get_picture_image(self, obj):
        return format_html(
            f'<img src="{obj.picture.url}" width="200" height=200 />'
        )


@admin.register(Place_picture)
class Place_PictureAdmin(admin.ModelAdmin):
    try:
        readonly_fields = [
            'get_picture_image',
        ]

        def get_picture_image(self, obj):
            return format_html(
                f'<img src="{obj.picture.url}" width="200" height=200 />'
            )
    except Exception as err:
        print(Exception, err)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    try:
        inlines = [
            Place_pictureInLine
        ]
    except Exception as err:
        print(Exception, err)

# Register your models here.
