from typing import Union
import requests
import time
import os


PUBLIC_KEY = os.environ.get("STRIPE_PK")
SECRET_KEY = os.environ.get("STRIPE_SK")


class StripeClient:
    # todo прописать свой хост
    def __init__(self):
        self.base_url = "https://api.stripe.com/v1"
        self.host = "http://localhost:8000"
        self.api_key = SECRET_KEY
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
                "quantity": i["quantity"]
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

        return line_items_dict

    def create_checkout_session(self, mode: str, customer_email: str, line_items: list = None) -> dict:
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
            "expires_at": int(time.time() + 30 * 60)
        }
        line_items_keys = self._get_line_items_dict(line_items)
        payload.update(line_items_keys)

        try:
            r = requests.post(url, data=payload, headers=self.headers, timeout=30)
            if r.status_code != 200:
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

#
# items = [{"title": "test one", "price": 900, "quantity": 1},
#          {"title": "test two", "price": 120, "quantity": 3},
#          {"title": "test three", "price": 24.7, "quantity": 2}]
# print("STRIPE TEST:", StripeClient().create_checkout_session(mode="payment", customer_email="tester@gmail.com", line_items=items))
#
