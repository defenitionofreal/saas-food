import os


def delete_old_file(path_file):
    """ Delete old file"""
    if os.path.exists(path_file):
        os.remove(path_file)
