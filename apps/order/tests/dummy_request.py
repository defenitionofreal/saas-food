from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest

from apps.order.services.generate_cart_key import _generate_cart_key


class DummyRequest(HttpRequest):
    def __init__(self, method='get', user=None, cart_session_id=None, generate_cart_id=False):
        super().__init__()
        self.method = method
        self.session = SessionBase()
        self.user = user
        if cart_session_id:
            self.session[settings.CART_SESSION_ID] = cart_session_id
            self.session.modified = True
        else:
            if generate_cart_id:
                self.session[settings.CART_SESSION_ID] = _generate_cart_key()
                self.session.modified = True

    def get_cart_session_id(self):
        return self.session.get(settings.CART_SESSION_ID)
