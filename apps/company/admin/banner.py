from django.contrib import admin
from apps.company.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    autocomplete_fields = ("institutions",)
