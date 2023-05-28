from django.contrib import admin
from apps.base.models import CustomUser, MessageLog, WeekDay
from rest_framework_simplejwt.tokens import OutstandingToken


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("phone", "email", "is_customer", "is_organization",
                    "is_superuser")

    def BE_AWARE_NO_WARNING_clear_tokens_and_delete(self, request, queryset):
        users = queryset.values("id")
        OutstandingToken.objects.filter(user__id__in=users).delete()
        queryset.delete()

    actions = ["BE_AWARE_NO_WARNING_clear_tokens_and_delete"]


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "get_type", "get_status")
    readonly_fields = ("created_at",)


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ("id", "title", "position")
