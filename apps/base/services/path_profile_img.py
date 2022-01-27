from apps.base.services.salt_generator import create_salt_generator


def get_path_profile(instance, image):
    """ Path to a profile  (media)/123-123/profile/ """
    return f'{instance.pk}/profile/{create_salt_generator(7)}_{image}'
