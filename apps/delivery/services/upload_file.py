from apps.base.services.salt_generator import create_salt_generator


def get_path_upload_map_file(instance, file):
    """ Path to a file  (media)/user@mail.com/map/ """
    return f'{instance.institution.user.email}/map/{create_salt_generator(7)}_{file}'

