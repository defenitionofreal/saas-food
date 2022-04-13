from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('apps.base.urls', namespace='base')),
    # devide users
    path('api/customer/', include('apps.customer.urls', namespace='customer')),
    path('api/organization/', include('apps.organization.urls', namespace='organization')),
    # showcase site
    path('api/showcase/<str:domain>/', include('apps.showcase.urls', namespace='showcase')),
]

urlpatterns += doc_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
