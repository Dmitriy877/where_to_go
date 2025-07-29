from django.contrib import admin
from places.models import Place, Place_picture
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableTabularInline


class Place_pictureInLine(SortableTabularInline, admin.TabularInline):
    model = Place_picture
    readonly_fields = [
            'get_picture_image',
        ]

    def get_picture_image(self, obj):
        picture_url = obj.picture.url
        return format_html(
            '<img src={} width="200" height=200 />',
            picture_url,
        )


@admin.register(Place_picture)
class Place_PictureAdmin(SortableAdminMixin, admin.ModelAdmin):
    try:
        readonly_fields = [
            'get_picture_image',
        ]

        def get_picture_image(self, obj):
            picture_url = obj.picture.url
            return format_html(
                '<img src={} style="max-height:200; max-width=:200;" />',
                picture_url,
            )
    except Exception as err:
        print(Exception, err)


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    try:
        inlines = [
            Place_pictureInLine
        ]
    except Exception as err:
        print(Exception, err)
