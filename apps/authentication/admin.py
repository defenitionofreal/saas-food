from django.contrib import admin
from apps.authentication.models import VerificationCode


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "code", "phone", "email", "is_confirmed", "is_active")
    readonly_fields = ("created_at", )
