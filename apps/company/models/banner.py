from django.db import models


class Banner(models.Model):
    """
    Promo banners on the main page
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="banner")
    image = models.ImageField(
        upload_to='images/users/')  # images/users/self.user/banners/
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    products = models.ManyToManyField("product.Product", blank=True, related_name="banner")
    promo_code = models.ForeignKey("order.PromoCode", on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name="banner")
    link = models.URLField(blank=True)
    link_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.title} на {self.institution}'
