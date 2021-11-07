from django.db import models


class Additive(models.Model):
    """
    Additive of the product
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="additives")
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField("media.Image", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
