from django.shortcuts import get_object_or_404
from rest_framework import viewsets, exceptions, response

from apps.company.models import Institution, Banner
from apps.showcase.serializers import BannerListSerializer, BannerDetailSerializer

import logging

logger = logging.getLogger(__name__)


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerListSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        domain = self.kwargs['domain']
        institution = get_object_or_404(
            Institution.objects.only("id", "domain"), domain=domain
        )
        queryset = super().get_queryset()
        return queryset.filter(institutions=institution).order_by('row')

    def retrieve(self, request, domain=None, pk=None):
        try:
            institution = get_object_or_404(
                Institution.objects.only("id", "domain"), domain=domain
            )
            query = get_object_or_404(
                Banner, institutions=institution, pk=pk, is_active=True
            )
            serializer = BannerDetailSerializer(query)
            return response.Response(serializer.data)
        except Institution.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Institution not found."})
        except Banner.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Banner not found."})
        except Exception as e:
            logger.error(f"error: {e}, request_data: {request.data}, domain: {domain}, slug: {slug}")
            raise exceptions.APIException({"detail": e})
