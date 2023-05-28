from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import SocialLinksSerializer
from apps.company.models import SocialLinks
from apps.authentication.permissions import ConfirmedAccountPermission


class SocialLinksViewSet(viewsets.ModelViewSet):
    queryset = SocialLinks.objects.all()
    serializer_class = SocialLinksSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(institution__user_id=self.request.user.id)
