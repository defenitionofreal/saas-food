from django.urls import path, include

app_name = 'customer'

urlpatterns = [
    path('', include('apps.base.urls', namespace='base')),
]
