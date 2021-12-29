from django.db import models


class DeliveryZone(models.Model):
    """
    Delivery zone model
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="delivery_zone")
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                           default=0)
    free_delivery_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                               default=0)
    delivery_time = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.institution} -> {self.title}'


class DeliveryZoneСoordinates(models.Model):
    """
    Delivery zone coordinates model
    """
    zone = models.ForeignKey(DeliveryZone, on_delete=models.CASCADE,
                             related_name="delivery_zone_coordinates")
    coordinates = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.zone}'
