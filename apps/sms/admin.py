from django.contrib import admin
from apps.sms.models import SmsLog


@admin.register(SmsLog)
class SmsLogAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "recipient", "phone", "sender", "text", "status")
