from django.contrib import admin
from apps.base.models import CustomUser, AuthCode, Sms, MessageLog


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("phone", "email", "is_customer", "is_organization",
                    "is_superuser")


@admin.register(AuthCode)
class AuthCodeAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("user", "code", "created_at", "updated_at", "is_active")


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "phone", "status",)


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "get_type", "get_status")
    readonly_fields = ("created_at",)
