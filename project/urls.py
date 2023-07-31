from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/base/', include('apps.base.urls', namespace='base')),  # todo: del ?
    path('api/authentication/', include('apps.authentication.urls', namespace='authentication')),
    # devide users
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
