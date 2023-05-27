from rest_framework.permissions import BasePermission
from apps.authentication.services.confirmed_account_checker import ConfirmedAccountChecker


class ConfirmedAccountPermission(BasePermission):
    def has_permission(self, request, view):
        return ConfirmedAccountChecker(request.user).check()
