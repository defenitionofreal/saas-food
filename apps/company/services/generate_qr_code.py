import qrcode
from django.conf import settings


def qrcode_generator(domain):
    """ QR code generator """
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=7,
        border=0,
    )
    # Version 5 is 37x37
    # (37 + 6 * 2) * 6 px = 294 px
    # At error correction mode Q, max size is 60 bytes
    text = f'{settings.ALLOWED_HOSTS[0]}/{domain}'
    if len(text) > 60:
        raise ValueError(
            'These QR code settings only support a max of 60 characters.'
        )
    qr.add_data(text)
    return qr.make_image(fill_color='black', back_color='white')

