import uuid


def check_if_list_exists_compare_values(request_list, institution_list):
    """
    Check if requested data is not blank
     - then check for a wrong uuid in a list
    """
    if request_list:
        if _find_wrong_inst_id(request_list, institution_list) is True:
            return True
    return False


def _find_wrong_inst_id(request_list, institution_list):
    """
    Checking for a wrong uuid
    """
    for i in request_list:
        if uuid.UUID(i) not in institution_list:
            return True
    return False


def _check_duplicated_uuid(request_list, model_field):
    """
    Checking for a value which is already exist in db
    """
    print("request_list", request_list)
    for i in request_list:
        print(model_field)
        if uuid.UUID(i) in model_field:
            return True
    return False
