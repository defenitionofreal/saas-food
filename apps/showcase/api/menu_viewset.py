from django.shortcuts import get_object_or_404
from rest_framework import viewsets, exceptions, response

from apps.company.models import Institution
from apps.product.models import Product
from apps.showcase.serializers import ProductListSerializer, ProductDetailSerializer

import logging

logger = logging.getLogger(__name__)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    http_method_names = ["get"]
    lookup_field = "slug"

    def get_queryset(self):
        domain = self.kwargs['domain']
        institution = get_object_or_404(
            Institution.objects.only("id", "domain"), domain=domain
        )
        queryset = super().get_queryset()
        return queryset.filter(institutions=institution).order_by('row')

    def retrieve(self, request, domain=None, slug=None):
        try:
            institution = get_object_or_404(
                Institution.objects.only("id", "domain"), domain=domain
            )
            query = get_object_or_404(
                Product, institutions=institution, slug=slug, is_active=True
            )
            serializer = ProductDetailSerializer(query)
            return response.Response(serializer.data)
        except Institution.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Institution not found."})
        except Product.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Product not found."})
        except Exception as e:
            logger.error(f"error: {e}, request_data: {request.data}, domain: {domain}, slug: {slug}")
            raise exceptions.APIException({"detail": e})
