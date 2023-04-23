import random
import string


def create_verification_code():
    """ код верификации для подтверждения телефона/почты """
    return "".join(random.choice(string.digits) for _ in range(4))
