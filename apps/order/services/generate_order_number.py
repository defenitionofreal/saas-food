import random
import string


def generate_order_number(letters_amount, digits_amount):
    """ function generates numbers like A-123 """
    digits = "".join(random.choices(string.digits, k=digits_amount))
    letters = "".join(random.choices(string.ascii_uppercase, k=letters_amount))
    return f"{letters}-{digits}"

