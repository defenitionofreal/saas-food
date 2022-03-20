from django.db import models


class ModifierPrice(models.Model):
    """
    Modifier price of the product
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="modifiers_price", null=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE,
                                related_name="modifiers_price")
    modifier = models.ForeignKey("product.Modifier", on_delete=models.CASCADE,
                                 related_name="modifiers_price")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'id:{self.id}: (inst. - {self.institution.domain})| {self.product.title}, {self.modifier} = {self.price}'
