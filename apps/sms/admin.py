from django.contrib import admin
from apps.sms.models import SmsLog, OrganizationSmsProvider


@admin.register(SmsLog)
class SmsLogAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "recipient", "phone", "sender", "text", "status")


@admin.register(OrganizationSmsProvider)
class OrganizationSmsProviderAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "user", "title", "is_active")
