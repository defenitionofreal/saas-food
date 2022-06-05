from django.db import models
from django.core.validators import FileExtensionValidator
from apps.delivery.services.upload_file import get_path_upload_map_file


class DeliveryZone(models.Model):
    """
    Delivery zone model
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="dz")
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=0)
    min_order_amount = models.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           default=0)
    free_delivery_amount = models.DecimalField(max_digits=10,
                                               decimal_places=2,
                                               default=0)
    delivery_time = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.institution} -> {self.title}'


class DeliveryZoneСoordinates(models.Model):
    """
    Delivery zone coordinates model
    """
    zone = models.ForeignKey(DeliveryZone,
                             on_delete=models.CASCADE,
                             related_name="dz_coordinates")
    coordinates = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.zone}'


class DeliveryZoneFile(models.Model):
    """
    Delivery zone kml file model
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="dz_file_institution")
    file = models.FileField(upload_to=get_path_upload_map_file,
                            validators=[FileExtensionValidator(
                                allowed_extensions=['kml'])])

    def __str__(self):
        return f'{self.institution} -> {self.file}'
