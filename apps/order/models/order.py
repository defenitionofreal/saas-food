from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from apps.payment.models.enums import PaymentType
from apps.order.models.enums.order_status import OrderStatus


User = get_user_model()


class Order(models.Model):
    """
    Order model (checkout) should contain:
    order method
    user address (if delivery method selected)
    institution address (if pick up method selected)
    payment type
    cart details with items (total price)
    generate code for e-queue
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="order_institution",
                                    null=True,
                                    blank=True)
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name="order_customer",
                                 null=True,
                                 blank=True)
    cart = models.OneToOneField("order.Cart",
                                on_delete=models.CASCADE,
                                related_name="order_cart",
                                null=True,
                                blank=True)
    payment_type = models.CharField(max_length=20,
                                    choices=PaymentType.choices,
                                    default=PaymentType.ONLINE)
    name = models.CharField(max_length=255, default="имя")
    phone = PhoneNumberField()
    comment = models.TextField(max_length=1000, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=10,
                              choices=OrderStatus.choices,
                              default=OrderStatus.PLACED)
    # paid field should be for an online payment only?
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            from apps.order.services.generate_order_number import \
                _generate_order_number
            self.code = _generate_order_number(1, 3)
        super().save(*args, **kwargs)

    @property
    def institution_name(self):
        return self.institution.title

    @property
    def delivery_type(self):
        return self.cart.delivery.type.delivery_type

    @property
    def delivery_address(self):
        address = {"city": self.cart.delivery.address.address.city,
                   "street": self.cart.delivery.address.address.street,
                   "building": self.cart.delivery.address.address.building,
                   "office": self.cart.delivery.address.address.office,
                   "floor": self.cart.delivery.address.address.floor}
        return address

    @property
    def delivery_date(self):
        return self.cart.delivery.order_date

    @property
    def delivery(self):
        delivery = {"type": self.delivery_type,
                    "address": self.delivery_address,
                    "order_date": self.delivery_date}
        return delivery

    @property
    def items(self):
        return self.cart.items.values("product", "quantity")

    @property
    def delivery_cost(self):
        cost = self.cart.get_delivery_price
        if self.cart.delivery.type.free_delivery_amount:
            if self.total_after_sale > self.cart.delivery.type.free_delivery_amount:
                cost = 0

        if self.cart.get_delivery_zone:
            cost = self.cart.get_delivery_zone["price"]
            if self.cart.get_delivery_zone["free_delivery_amount"]:
                if self.total_after_sale > self.cart.get_delivery_zone["free_delivery_amount"]:
                    cost = 0

        if self.cart.promo_code and self.cart.promo_code.delivery_free is True:
            cost = 0

        return cost

    @property
    def delivery_sale(self):
        return self.cart.get_delivery_sale

    @property
    def coupon_sale(self):
        return self.cart.get_sale

    @property
    def bonus_write_off(self):
        return self.cart.customer_bonus

    @property
    def bonus_accrual(self):
        return self.cart.get_bonus_accrual

    @property
    def total(self):
        return self.cart.get_total_cart

    @property
    def total_after_sale(self):
        return self.cart.get_total_cart_after_sale

    @property
    def final_price(self):
        return self.cart.final_price
