from decimal import Decimal


def get_absolute_from_percent_and_total(percent, total):
    return round((percent / Decimal('100')) * total)
