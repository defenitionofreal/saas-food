from rest_framework.permissions import BasePermission
from apps.authentication.services.confirmed_account_checker import ConfirmedAccountChecker


class ConfirmedAccountPermission(BasePermission):
    def has_permission(self, request, view):
        return ConfirmedAccountChecker(request.user).is_confirmed()


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return ConfirmedAccountChecker(request.user).is_customer()


class OrganizationPermission(BasePermission):
    def has_permission(self, request, view):
        return ConfirmedAccountChecker(request.user).is_organization()
