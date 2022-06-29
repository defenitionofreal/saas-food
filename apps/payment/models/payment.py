from django.db import models
from django.contrib.auth import get_user_model
from apps.payment.models.enums.payment_type import PaymentType
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
    institution = models.ForeignKey(Institution,
                                    on_delete=models.CASCADE,
                                    related_name="payment_inst",
                                    blank=True,
                                    null=True)
    # user as a customer
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="payment_user")
    order = models.ForeignKey("order.Order",
                              on_delete=models.CASCADE,
                              related_name="payment_order")
    # The payment id provided by the payment gateway
    code = models.CharField(max_length=255,
                            blank=True,
                            null=True)
    type = models.CharField(max_length=20,
                            choices=PaymentType.choices,
                            default=PaymentType.ONLINE)
    status = models.CharField(max_length=10,
                              choices=PaymentStatus.choices,
                              default=PaymentStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
