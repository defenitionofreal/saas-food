def get_path_upload_map_file(instance, file):
    """ Path to a file  (media)/user@mail.com/map/ """
    return f'{instance.institution.user.email}/map/{file}'
