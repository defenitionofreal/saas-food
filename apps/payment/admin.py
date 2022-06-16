from django.contrib import admin

from apps.payment.models import (PaymentTypeInstitution)


@admin.register(PaymentTypeInstitution)
class PaymentTypeInstitutionAdmin(admin.ModelAdmin):
    search_fields = ("id",)

