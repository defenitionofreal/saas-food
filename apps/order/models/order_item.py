from django.db import models


class OrderItem(models.Model):
    """
    Order items model
    """
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="order_item")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
