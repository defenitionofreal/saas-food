import random


def _generate_cart_key():
    """ function for generating random cart key values """
    cart_key = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_key += characters[random.randint(0, len(characters) - 1)]
    return cart_key
