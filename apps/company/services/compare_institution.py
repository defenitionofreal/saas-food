import uuid


def _find_wrong_inst_id(request_list, institution_list):
    """
    Checking for a wrong uuid
    """
    for i in request_list:
        if uuid.UUID(i) not in institution_list:
            return True
    return False
