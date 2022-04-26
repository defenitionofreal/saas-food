import uuid


def _compare_inst(request_list, institution_list):
    """
    Checking for a wrong uuid
    """
    for i in request_list:
        if uuid.UUID(i) not in institution_list:
            return False
    return True
