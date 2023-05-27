from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import SocialLinksSerializer
from apps.company.models import SocialLinks
from apps.authentication.permissions import ConfirmedAccountPermission


class SocialLinksViewSet(viewsets.ModelViewSet):
    queryset = SocialLinks.objects.all()
    serializer_class = SocialLinksSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    # todo: queryset для юзера, чтобы не видеть всех объектов, но есть связь только с филиалом
