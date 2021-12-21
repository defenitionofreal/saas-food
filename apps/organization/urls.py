from django.urls import path, include

app_name = 'organization'

urlpatterns = [
    path('', include('apps.base.urls', namespace='base')),
    path('institution/', include('apps.company.urls', namespace='company')),
    path('location/', include('apps.location.urls', namespace='location')),
    path('', include('apps.delivery.urls', namespace='delivery')),
]
