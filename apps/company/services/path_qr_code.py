from apps.base.services.salt_generator import create_salt_generator


def get_path_qr_code(instance):
    """ Path to a qr  (media)/user@mail.com/qr/ """
    return f'{instance.institution.user.pk}/qr/'