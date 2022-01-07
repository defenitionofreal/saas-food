def get_path_qr_code(instance, qrcode):
    """ Path to a qr  (media)/123-123/qr/ """
    return f'{instance.user.pk}/qrcode/{qrcode}'
