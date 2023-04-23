from django.contrib import admin
from apps.base.models import CustomUser, AuthCode, Sms, MessageLog


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("phone", "email", "is_customer", "is_superuser")


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
    list_display = ("id", "get_type_display", "get_status_display")
    readonly_fields = ("created_at",)

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_type_display(self, obj):
        return obj.get_type_display()
