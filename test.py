import random
import string


def gen_num():
    digits = "".join(random.choices(string.digits, k=3))
    return f"{random.choices(string.ascii_uppercase, k=1)[0]}-{digits}"


print(gen_num())
