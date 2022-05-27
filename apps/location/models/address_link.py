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
                                on_delete=models.CASCADE)
    # session_id ?
