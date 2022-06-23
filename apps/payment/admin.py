from django.contrib import admin

from apps.payment.models import (PaymentTypeInstitution,
                                 YooMoney)


@admin.register(PaymentTypeInstitution)
class PaymentTypeInstitutionAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(YooMoney)
class YooMoneyAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "wallet"]
    search_fields = ("id",)

