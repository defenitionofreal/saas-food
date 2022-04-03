from django.contrib import admin

from apps.order.models import UserBonus


@admin.register(UserBonus)
class UserBonusAdmin(admin.ModelAdmin):
    search_fields = ("id",)
