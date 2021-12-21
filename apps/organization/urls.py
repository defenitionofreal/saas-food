from django.urls import path, include

app_name = 'organization'

urlpatterns = [
    path('', include('apps.base.urls', namespace='base')),
    path('institution/', include('apps.company.urls', namespace='company')),
    path('', include('apps.delivery.urls', namespace='delivery')),
    path('', include('apps.product.urls', namespace='product')),
]
