from django.db import models
from django.contrib.auth import get_user_model
from apps.payment.models.enums.payment_status import PaymentStatus
from apps.company.models import Institution
import uuid

User = get_user_model()


class Payment(models.Model):
    """
    Payment model
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    order = models.ForeignKey("order.Cart",
                              on_delete=models.CASCADE,
                              related_name="payment_order")
    code = models.CharField(max_length=255,
                            blank=True,
                            null=True,
                            help_text="The payment id provided by the payment gateway")
    status = models.CharField(max_length=10,
                              choices=PaymentStatus.choices,
                              default=PaymentStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def payment_type(self):
        return self.order.payment_type

    @property
    def customer(self):
        return self.order.customer

    @property
    def institution(self):
        return self.order.institution

    @property
    def total_order_price(self):
        return self.order.get_total_cart

    @property
    def final_price(self):
        return self.order.final_price
