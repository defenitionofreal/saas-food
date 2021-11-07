from django.contrib import admin
from apps.company.models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    search_fields = ("title",)
