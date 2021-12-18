from django.urls import path, include

app_name = 'organization'

urlpatterns = [
    path('', include('apps.base.urls', namespace='base')),
    path('', include('apps.company.urls', namespace='company')),
]
