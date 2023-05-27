from apps.base.services.salt_generator import create_salt_generator


def get_path_banner(instance, image):
    """ Path to a banners  (media)/123-123/banners/ """
    return f'{instance.user.pk}/banners/{create_salt_generator(7)}_{image}'
