from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal


User = get_user_model()


class CartDeliveryInfo(models.Model):
    cart = models.ForeignKey(
        "order.Cart",
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        "delivery.DeliveryTypeRule",
        on_delete=models.CASCADE
    )
    zone = models.ForeignKey(
        "delivery.DeliveryZone",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Delivery zone if exists and delivery type is courier"
    )
    customer_address = models.ForeignKey(
        "delivery.CustomerAddress",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="address filled if delivery type is courier"
    )
    institution_address = models.ForeignKey(
        "delivery.InstitutionAddress",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="address filled if delivery type is pickup or indoor"
    )
    delivery_date = models.DateField(
        blank=True,
        null=True
    )
    delivery_time = models.TimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.id}: {self.type}"

    @property
    def delivery_price(self) -> Decimal:
        """ zone has priority above default delivery rule """
        return self.zone.price if self.zone else self.type.delivery_price

    @property
    def free_delivery_amount(self) -> Decimal:
        """ zone has priority above default delivery rule """
        return self.zone.free_delivery_amount if self.zone else self.type.free_delivery_amount

    @property
    def min_delivery_order_amount(self) -> int:
        return self.zone.min_order_amount if self.zone else self.type.min_order_amount

    @property
    def delivery_sale(self) -> int:
        """ sale sum """
        delivery_sale = self.type.sale_amount
        if delivery_sale:
            if self.type.sale_type == "percent":
                total_with_sale = self.cart.get_total_with_sale
                delivery_sale = round((delivery_sale / Decimal("100")) * total_with_sale)
            if self.type.sale_type == "absolute":
                delivery_sale = delivery_sale
        return delivery_sale

    @property
    def final_delivery_price(self) -> Decimal:
        """ price sum """
        price = self.delivery_price
        if self.cart.get_total_with_sale >= self.free_delivery_amount:
            price = Decimal("0")
        if self.cart.promo_code and self.cart.promo_code.delivery_free:
            price = Decimal("0")
        return price
