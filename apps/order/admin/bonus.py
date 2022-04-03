from django.contrib import admin

from apps.order.models import Bonus


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    search_fields = ("id",)
