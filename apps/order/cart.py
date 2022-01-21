# https://pocoz.gitbooks.io/django-v-primerah/content/glava-7-sozdanie-internet-magazina/sozdanie-korzini/nastroiki-sessii.html

from decimal import Decimal
from django.conf import settings
from apps.product.models import Product
from apps.order.models import PromoCode, OrderItem


class Cart:
    def __init__(self, user, order, institution):
        self.user = user
        self.order = order
        self.institution = institution
        self.cart_base_total_amount = 0
        self.cart_final_total_amount = 0
        self.campaign_discount_amounts = []
        self.campaign_discount_amount = 0
        self.coupon_discount_amount = 0
        self.delivery_cost = 0
        self.order_items = []
        self.discounts = {}
        self.checkout_details = {'products': [], 'total': [], 'amount': []}

    def prepare_cart_for_checkout(self):
        self.order_items = OrderItem.objects.filter(order=self.order)

        if not self.order_items:
            return False

        self.calculate_cart_base_total_amount()
        # self.get_delivery_cost()
        # self.get_campaign_discounts()
        # self.get_coupon_discounts()
        # self.calculate_discount_amounts()
        # self.get_total_amount_after_discounts()
        # self.prepare_checkout_details()

    def calculate_cart_base_total_amount(self):
        for order_items in self.order_items:
            self.cart_base_total_amount += order_items.product.price * order_items.quantity

    def prepare_checkout_details(self):
        for order_items in self.order_items:
            self.checkout_details['products'].append(
                {'category_id': order_items.product.category.id,
                 'category_name': order_items.product.category.title,
                 'product_id': order_items.product.id,
                 'product_name': order_items.product.title,
                 'quantity': order_items.quantity,
                 'product_price': order_items.product.price})

        # self.checkout_details['total'].append(
        #     {'total_price': self.cart_base_total_amount,
        #      'total_discount':
        #          self.campaign_discount_amount + self.coupon_discount_amount})
        #
        # self.checkout_details['amount'].append(
        #     {'total_amount': self.cart_final_total_amount,
        #      'delivery_cost': self.delivery_cost})

