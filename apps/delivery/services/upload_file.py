from apps.base.services.salt_generator import create_salt_generator


def get_path_upload_map_file(instance, file):
    """ Path to a file  (media)/123-123/map/ """
    return f'{instance.institution.user.pk}/map/{create_salt_generator(7)}_{file}'

