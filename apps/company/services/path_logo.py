def get_path_logo(instance, logo):
    """ Path to a logo """
    return f'{instance.user.pk}/logo/{logo}'
