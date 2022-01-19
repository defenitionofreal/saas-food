from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    """
    Order model (checkout) should contain:
    order method
    user address (if delivery method selected)
    institution address (if pick up method selected)
    payment type
    cart details with items (total price)
    generate code for e-queue
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="order_institution", null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="order_customer", null=True, blank=True)
    phone = PhoneNumberField()
    address = models.ForeignKey("location.Address", on_delete=models.SET_NULL,
                                related_name="order_address", null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(max_length=1000, blank=True)
    date_delivery = models.DateTimeField(blank=True,
                                         null=True)  # время доставки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
