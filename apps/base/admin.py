from django.contrib import admin
from apps.base.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    ordering = ("email", "phone", "pk")
