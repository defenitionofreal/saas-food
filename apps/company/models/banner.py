from django.db import models
from apps.company.services.path_banner import get_path_banner
from django.core.validators import FileExtensionValidator


class Banner(models.Model):
    """
    Promo banners on the main page
    """
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        blank=True,
        related_name="banner"
    )
    image = models.ImageField(upload_to=get_path_banner,
                              validators=[FileExtensionValidator(
                                  allowed_extensions=['jpg', 'jpeg', 'png'])])
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    products = models.ManyToManyField("product.Product", blank=True,
                                      related_name="banner")
    promo_code = models.ForeignKey("order.PromoCode",
                                   on_delete=models.SET_NULL,
                                   blank=True, null=True,
                                   related_name="banner")
    link = models.URLField(blank=True)
    link_text = models.CharField(max_length=100, blank=True)
    row = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} на {self.institution}'
