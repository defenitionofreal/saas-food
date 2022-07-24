from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F

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
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='cart_customer',
                                 null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promo_code = models.ForeignKey("order.PromoCode",
                                   on_delete=models.SET_NULL,
                                   related_name="cart_promo_code",
                                   null=True,
                                   blank=True)
    customer_bonus = models.PositiveIntegerField(blank=True,
                                                 null=True)
    delivery = models.ForeignKey("delivery.DeliveryInfo",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="cart_delivery")
    min_amount = models.PositiveIntegerField(blank=True,
                                             null=True)
    items = models.ManyToManyField("order.CartItem",
                                   related_name="cart_items")
    session_id = models.CharField(max_length=50,
                                  blank=True,
                                  null=True,
                                  unique=True)

    @property
    def get_total_cart(self):
        return sum(i.get_total_item_price for i in self.items.all())

    def __str__(self):
        return f'Cart {self.id}: {self.institution} -> {self.customer}, {self.get_total_cart}'

    def __iadd__(self, other):
        if not isinstance(other, Cart):
            return
        other_items = other.items.all()
        print(other_items)
        for i in other_items:
            product_dict = i.product
            quantity = i.quantity
            self.add_item(product_dict, quantity)
        return self

    def add_item(self, product_dict: dict, quantity=1):
        """ add new item to cart or update quantity of an item """
        from apps.order.models import CartItem
        cart_item, cart_item_created = CartItem.objects.get_or_create(product=product_dict,
                                                                      cart=self)

        if self.items.filter(product=product_dict).exists():
            cart_item.quantity = F("quantity") + quantity
            cart_item.save(update_fields=("quantity",))
        else:
            cart_item.quantity = quantity
            cart_item.save()
            self.items.add(cart_item)
