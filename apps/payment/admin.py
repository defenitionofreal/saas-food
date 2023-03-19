from django.contrib import admin

from apps.payment.models import (PaymentTypeInstitution,
                                 Payment,
                                 YooMoney,
                                 StripeIntegration)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "order", "institution", "customer", "final_price"]
    search_fields = ("id",)


@admin.register(PaymentTypeInstitution)
class PaymentTypeInstitutionAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(YooMoney)
class YooMoneyAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "wallet"]
    search_fields = ("id",)


@admin.register(StripeIntegration)
class StripeIntegrationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "api_key"]
    search_fields = ("id",)

