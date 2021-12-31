import random
import string


def create_salt_generator(num):
    numbers = string.digits
    alpha = string.ascii_letters
    symbol = string.punctuation
    output = []
    new_pass = list(zip(alpha, symbol, numbers))
    for item in new_pass:
        for i in item:
            output.append(i)

    generate = ''.join(random.choices(output, k=num))
    return generate
