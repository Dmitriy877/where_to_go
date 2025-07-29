from django.contrib import admin
from places.models import Place, PlacePicture
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableTabularInline


class PlacePictureInLine(SortableTabularInline, admin.TabularInline):
    model = PlacePicture
    readonly_fields = [
            'get_picture_image',
        ]

    def get_picture_image(self, obj):
        picture_url = obj.picture.url
        return format_html(
            '<img src={} width=200 height=200 />',
            picture_url,
        )


@admin.register(PlacePicture)
class PlacePictureAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = [
        'get_picture_image',
    ]
    raw_id_fields = [
        'place',
    ]

    def get_picture_image(self, obj):
        picture_url = obj.picture.url
        return format_html(
            '<img src={} width=200 height=200 />',
            picture_url,
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [
        PlacePictureInLine
    ]
