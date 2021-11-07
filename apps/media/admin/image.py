from django.contrib import admin
from apps.media.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ("title",)
