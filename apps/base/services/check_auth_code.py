from apps.base.models import AuthCode


def check_auth_code(user, code):
    """
    Find the current active code
    Check if code is using to authenticate
    After authentication make this code active=False
    """
    auth_code = (AuthCode.objects.active().filter(user=user,
                                                  code=code, ).first())

    if auth_code:
        auth_code.is_active = False
        auth_code.save()
        is_valid = True
    else:
        is_valid = False

    return is_valid
