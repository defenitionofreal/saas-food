from django.utils.baseconv import BASE62_ALPHABET
from django.utils.crypto import get_random_string

CHARACTERS = f"{BASE62_ALPHABET}!@#$%^&*()"


def _generate_cart_key():
    """ function for generating random cart key values """
    cart_key_length = 50
    return get_random_string(cart_key_length, CHARACTERS)
