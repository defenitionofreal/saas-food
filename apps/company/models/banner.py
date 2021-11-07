from django.db import models


class Banner(models.Model):
    """
    Promo banners on the main page
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="banner")
    image = models.ImageField(upload_to='images/users/')  # images/users/self.user/banners/
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    # products = models.ForeignKey()  # products in a promo
    # promo_code = models.ForeignKey()  # code in a promo
    link = models.URLField()
    link_text = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title} на {self.institution}'

