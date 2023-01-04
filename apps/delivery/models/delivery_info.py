from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class DeliveryInfo(models.Model):
    """
    Model for a user with customer role
    """
    # delivery info of a user if authorized
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    # user could choose a type from given
    type = models.ForeignKey("delivery.Delivery",
                             on_delete=models.CASCADE)
    # address filled if delivery type is delivery else auto replacement
    address = models.ForeignKey("location.AddressLink",
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True)
    # customer could choose date & time of an order (optional)
    order_date = models.DateTimeField(blank=True, null=True)
    # if user is guest
    session_id = models.CharField(max_length=50,
                                  blank=True,
                                  null=True)

    def __str__(self):
        return f"{self.id}: {self.type}"
