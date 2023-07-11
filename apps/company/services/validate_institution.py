from rest_framework.exceptions import ValidationError


def validate_institution_list(request_data, institution_qs, instance_qs, check_duplicate=False):
    """
    Validate institution data.
    Request list is requested data for institution field.

    Check if affiliate id is valid and also has possibility to check
    if affiliate is already related to some object.
    """
    if not request_data:
        raise ValidationError({"detail": "Request data is required."})

    institution_id_list = list(institution_qs.values_list("id", flat=True))
    if isinstance(request_data, list):
        instance_institution_list = list(instance_qs.values_list("institutions", flat=True))
    else:
        instance_institution_list = list(instance_qs.values_list("institution", flat=True))

    _validate_list(request_data, institution_id_list, instance_institution_list, check_duplicate)


def _validate_list(request_data, institution_id_list, instance_institution_list, check_duplicate: bool):
    """ """

    institution_list = [str(inst_id) for inst_id in institution_id_list]
    obj_model_field = [str(inst_id) for inst_id in instance_institution_list]

    if isinstance(request_data, list):
        for i in request_data:
            # If institution id not in institution_list, then its wrong id.
            if str(i.id) not in institution_list:
                raise ValidationError({"detail": "Wrong institution id."})
            # If institution id already at obj values, then its duplicated.
            if check_duplicate and str(i.id) in obj_model_field:
                raise ValidationError({"detail": f"Object already related."})
    else:
        if str(request_data.id) not in institution_list:
            raise ValidationError({"detail": "Wrong institution id."})
        if check_duplicate and str(request_data.id) in obj_model_field:
            raise ValidationError({"detail": "Object already related."})
