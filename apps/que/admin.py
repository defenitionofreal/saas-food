from django.contrib import admin
from apps.que.models import Que


@admin.register(Que)
class QueAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "order_id", "status")
    readonly_fields = ("created_at",)
