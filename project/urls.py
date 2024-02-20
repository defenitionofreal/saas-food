from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from project.yasg import urlpatterns as swagger_urls

# TODO: УБРАТЬ ПУТИ ОТ ORGANIZATION, CUSTOMER И SHOWCASE.
#  СДЕЛАТЬ из в путях от приложений как:
#  delivery/organization... ,  delivery/customer... и так далее  !!!
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include('apps.base.urls', namespace='base')),
    path('authentication/', include('apps.authentication.urls', namespace='authentication')),
    path('customer/', include('apps.customer.urls', namespace='customer')),
    path('showcase/', include('apps.showcase.urls', namespace='showcase')),  # todo? оставить или попереносить вьюшки?
    path('order/', include('apps.order.urls', namespace='order')),
    path('company/', include('apps.company.urls', namespace='company')),
    path('delivery/', include('apps.delivery.urls', namespace='delivery')),
    path('product/', include('apps.product.urls', namespace='product')),
    path('payment/', include('apps.payment.urls', namespace='payment')), # webhook?
]

urlpatterns += swagger_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
