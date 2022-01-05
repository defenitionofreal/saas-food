from apps.base.services.salt_generator import create_salt_generator


def get_path_qr_code(instance):
    """ Path to a qr  (media)/123-123/qr/ """
    return f'{instance.institution.user.pk}/qrcode/'