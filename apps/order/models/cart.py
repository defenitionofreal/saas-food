from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    """
    A model that contains data for a shopping cart.
    Minimum amount at cart (if added)
    delivery cost (if added) ?! or in order model?
    promo code (coupon) for sale
    add bonus points to a customer profile or he could spend his points
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="cart_institution")
    customer = models.OneToOneField(User, on_delete=models.CASCADE,
                                    related_name='cart_customer',
                                    null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promo_code = models.ForeignKey("order.PromoCode", on_delete=models.SET_NULL,
                                   related_name="cart_promo_code", null=True,
                                   blank=True)
    customer_bonus = models.ForeignKey("order.Bonus", on_delete=models.SET_NULL,
                                       blank=True, null=True,
                                       related_name="cart_bonus")
    #delivery_cost = models.
    min_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    items = models.ManyToManyField("order.CartItem", related_name="cart_items")

    @property
    def get_total_cart(self):
        total = 0
        for i in self.items.all():
            total += i.get_single_item_total
        return total

    def __str__(self):
        return f'Cart: {self.institution} -> {self.customer}, {self.get_total_cart}'
