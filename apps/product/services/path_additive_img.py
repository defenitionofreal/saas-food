from apps.base.services.salt_generator import create_salt_generator


def get_path_additive(instance, image):
    """ Path to an additive  (media)/123-123/additives/ """
    return f'{instance.institution.user.pk}/additives/{create_salt_generator(7)}_{image}'