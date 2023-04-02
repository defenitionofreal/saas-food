import random
import string
import datetime
from apps.order.models.cart import Cart


def generate_order_number(institution_id: int):
    """
    Function generates numbers like T-614 and so on.
    Number stays unique for institution and wont repeat on the same day.
    """
    today = datetime.date.today()

    latest_order = Cart.objects.filter(
        created_at__date=today,
        institution_id=institution_id).order_by("-code").first()

    if latest_order:
        last_number = int(latest_order.code.split('-')[-1])
    else:
        last_number = 0
    new_number = last_number + 1

    digits = str(new_number).zfill(3)
    letters = "".join(random.choices(string.ascii_uppercase, k=1))

    return f"{letters}-{digits}"
