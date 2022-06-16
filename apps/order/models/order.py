from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from apps.payment.models.enums import PaymentType

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
                                    related_name="order_institution",
                                    null=True,
                                    blank=True)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name="order_customer",
                                 null=True,
                                 blank=True)
    cart = models.OneToOneField("order.Cart",
                                on_delete=models.CASCADE,
                                related_name="order_cart",
                                null=True,
                                blank=True)

    payment_type = models.CharField(max_length=20,
                                    choices=PaymentType.choices,
                                    default=PaymentType.ONLINE)

    name = models.CharField(max_length=255, default="имя")
    phone = PhoneNumberField()
    comment = models.TextField(max_length=1000, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
