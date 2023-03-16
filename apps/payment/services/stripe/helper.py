from typing import Union
import requests
import time
import os
import hashlib
import hmac
import json

from django.http import HttpResponse

from apps.order.models.cart import Cart
from apps.order.models.enums.order_status import OrderStatus
from apps.payment.models.payment import Payment
from apps.payment.models.enums.payment_status import PaymentStatus


PUBLIC_KEY = os.environ.get("STRIPE_PK")
SECRET_KEY = os.environ.get("STRIPE_SK")


class StripeClient:
    # todo прописать свой хост
    def __init__(self, host: str, api_key: str):
        self.base_url = "https://api.stripe.com/v1"
        self.host = host  # ссылка филиала
        self.api_key = api_key  # ключ компании
        self.headers = {"Content-Type": "application/x-www-form-urlencoded",
                        "Authorization": f"Bearer {self.api_key}"}

    @staticmethod
    def _valid_price_format(price: Union[int, float]) -> int:
        """
        In Stripe, prices are represented in the smallest unit of currency
        To format a price value to the Stripe format, multiply the price by 100
        """
        return int(price * 100)

    @classmethod
    def _get_line_items_list(cls, line_items: list) -> list:
        """
        Get product items list and form a new items list for Stripe params
        """
        items_list = []
        for i in line_items:
            product = {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": i["title"]},
                    "unit_amount": cls._valid_price_format(i["price"])
                },
                "quantity": i["quantity"],
                "description": i["description"]
            }
            items_list.append(product)

        return items_list

    @classmethod
    def _get_line_items_dict(cls, line_items: list) -> dict:
        """
        Form a dictionary with each item with index because Stripe uses
        x-www-form-urlencoded format
        """
        items_list = cls._get_line_items_list(line_items)

        line_items_dict = {}
        for i, line_item in enumerate(items_list):
            line_items_dict[f"line_items[{i}][price_data][product_data][name]"] = line_item["price_data"]["product_data"]["name"]
            line_items_dict[f"line_items[{i}][price_data][unit_amount]"] = line_item["price_data"]["unit_amount"]
            line_items_dict[f"line_items[{i}][price_data][currency]"] = line_item["price_data"]["currency"]
            line_items_dict[f"line_items[{i}][quantity]"] = line_item["quantity"]
            # for j, option in enumerate(line_item.get("options", [])):
            #     line_items_dict[f"line_items[{i}][price_data][product_data][options][{j}][name]"] = option.get("name")
            #     line_items_dict[f"line_items[{i}][price_data][product_data][options][{j}][value]"] = option.get("value")

        return line_items_dict

    def create_checkout_session(self, mode: str, customer_email: str,
                                line_items: list = None,
                                order_id: str = None) -> dict:
        """

        doc.url: https://stripe.com/docs/api/checkout/sessions
        """
        modes = ("payment", "setup", "subscription")
        if (mode not in modes) or (not line_items):
            message = {"status": "error",
                       "status_code": 400,
                       "message": "Wrong mode or empty line items"}
            return message

        url = self.base_url + "/checkout/sessions"
        success_url = self.host + "/success"
        cancel_url = self.host + "/cancel"

        payload = {
            "payment_method_types[]": ["card"],
            "success_url": success_url,
            "cancel_url": cancel_url,
            "mode": mode,
            "customer_email": customer_email,
            "expires_at": int(time.time() + 30 * 60),
            "metadata[order_id]": order_id if order_id else "",
            "payment_intent_data[metadata][order_id]": order_id if order_id else ""
        }
        line_items_keys = self._get_line_items_dict(line_items)
        payload.update(line_items_keys)

        try:
            r = requests.post(url, data=payload, headers=self.headers, timeout=30)
            if r.status_code != 200:
                print("YOOO",  r.json())
                message = {"status": "error",
                           "status_code": r.status_code,
                           "message": r.json()["error"]["message"]}
            else:
                message = {"status": "success",
                           "status_code": r.status_code,
                           "message": r.json()["url"]}
            return message
        except Exception as e:
            message = {"status": "error",
                       "status_code": 500,
                       "message": f"{e}"}
            return message

    @staticmethod
    def _construct_webhook_event(payload, sig_header, endpoint_secret):
        """ """
        signatures = sig_header.split(',')
        timestamp = int(signatures[0].split('=')[1])
        body = payload.decode('utf-8')

        expected_signature = hmac.new(
            endpoint_secret.encode(),
            f"{timestamp}.{body}".encode(),
            hashlib.sha256
        ).hexdigest()

        for signature in signatures[1:]:
            if hmac.compare_digest(signature.split('=')[1], expected_signature):
                return json.loads(body)
        # If none of the signatures match, reject the request.
        return None

    def webhook(self, request):
        """  """
        endpoint_secret = "whsec_fa3f8e842e1fac92660338c86439c0fe730a997055a13bc24902d1e245a8719e"

        if request.method == 'POST':
            payload = request.body
            sig_header = request.META['HTTP_STRIPE_SIGNATURE']
            event = None
            try:
                event = self._construct_webhook_event(
                    payload, sig_header, endpoint_secret
                )
            except ValueError as e:
                # Invalid payload
                return HttpResponse(status=400)

            # Handle the events

            # if event["type"] == "checkout.session.completed":
            #     from apps.order.models.cart import Cart
            #     data = event["data"]["object"]
            #     order_id = data["metadata"]["order_id"]
            #     order = Cart.objects.get(id=order_id)
            #     print("ORDER OBJ", order)

            if event["type"] == 'charge.succeeded':
                charge = event["data"]["object"]
                order_id = charge["metadata"]["order_id"]
                # order
                order = Cart.objects.get(id=order_id)
                order.paid = True
                order.status = OrderStatus.ACCEPTED
                order.save()
                # payment
                payment = Payment.objects.get(order_id=order.id)
                payment.status = PaymentStatus.SUCCESS
                # todo: add payment.code
                payment.save()

            if event["type"] == 'charge.failed':
                charge = event["data"]["object"]
                order_id = charge["metadata"]["order_id"]
                # payment
                payment = Payment.objects.get(order_id=order_id)
                payment.status = PaymentStatus.FAILED
                # todo: add payment.code
                payment.save()
