from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AddressLink(models.Model):
    """
    Address link model
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    address = models.ForeignKey("location.Address",
                                on_delete=models.CASCADE,
                                related_name="address")
    # if user is a guest
    session_id = models.CharField(max_length=50,
                                  blank=True,
                                  null=True,
                                  unique=True)

    def __str__(self):
        return f"User ID: {self.user.id if self.user else None} | Address: {self.address}"
