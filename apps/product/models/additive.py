from django.db import models


class CategoryAdditive(models.Model):
    """
    Category of additive
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="category")
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    row = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Additive(models.Model):
    """
    Additive of the product
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="additives")
    category = models.ForeignKey(CategoryAdditive, on_delete=models.SET_NULL,
                                 null=True, related_name="category_additive")
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField("media.Image", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.title
