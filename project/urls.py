from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.generators import OpenAPISchemaGenerator

from .yasg import urlpatterns as doc_urls

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Food API",
      default_version='v1',
      description=""
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/base/', include('apps.base.urls', namespace='base')),
    path('api/authentication/', include('apps.authentication.urls', namespace='authentication')),
    # split users
    path('api/customer/', include('apps.customer.urls', namespace='customer')),
    path('api/organization/', include('apps.organization.urls', namespace='organization')),
    # showcase site
    path('api/showcase/', include('apps.showcase.urls', namespace='showcase')),
    # payment (for webhooks)
    path('webhook/', include('apps.payment.urls', namespace='payment')),
]

urlpatterns += doc_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
