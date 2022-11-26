from django.urls import path, include
from apps.showcase.api import (products_client_list,
                               categories_client_list,
                               categories_client_detail,
                               banners_client_list,
                               banners_client_detail,
                               analytics_client_list,
                               design_client_detail,
                               social_links_client_list,
                               extra_phone_client_list,
                               working_hours_client_list,
                               requisites_client_list,
                               products_client_detail,
                               delivery_client_list,
                               address_list,
                               delivery_zone_list,
                               payment_type_list)

from apps.showcase.api.customer_actions import (delivery_info_create)

app_name = 'showcase'

urlpatterns = [
    # main page
    path('<str:domain>/menu/', products_client_list.ProductsClientListAPIView.as_view()),
    path('<str:domain>/categories/', categories_client_list.CategoriesClientListAPIView.as_view()),
    path('<str:domain>/categories/<str:slug>/', categories_client_detail.CategoriesClientDetailAPIView.as_view()),
    path('<str:domain>/banners/', banners_client_list.BannersClientListAPIView.as_view()),
    path('<str:domain>/analytics/', analytics_client_list.AnalyticsClientListAPIView.as_view()),

    # TODO: change design to create or update view so no pk in url !
    path('<str:domain>/design/<int:pk>/', design_client_detail.DesignClientDetailAPIView.as_view()),

    # main page pop ups
    # banner
    path('<str:domain>/banners/<int:pk>/', banners_client_detail.BannersClientDetailAPIView.as_view()),
    # product
    path('<str:domain>/menu/<str:slug>/', products_client_detail.ProductClientDetailAPIView.as_view()),

    # company info
    path('<str:domain>/social-links/', social_links_client_list.SocialLinksClientListAPIView.as_view()),
    path('<str:domain>/extra-phones/', extra_phone_client_list.ExtraPhoneClientListAPIView.as_view()),
    path('<str:domain>/working-hours/', working_hours_client_list.WorkingHoursClientListAPIView.as_view()),
    path('<str:domain>/requisites/', requisites_client_list.RequisitesClientListAPIView.as_view()),

    # order (cart) detail/add/delete
    path('<str:domain>/order/', include('apps.order.urls', namespace='order')),
    # payment
    path('payment/', include('apps.payment.urls', namespace='payment')),
    # delivery
    path('<str:domain>/delivery/', delivery_client_list.DeliveryClientListAPIView.as_view()),
    path('<str:domain>/delivery-info/add/', delivery_info_create.DeliveryInfoAPIView.as_view()),
    path('<str:domain>/address/', address_list.AddressListAPIView.as_view()),
    path('<str:domain>/delivery-zone/', delivery_zone_list.DeliveryZoneListAPIView.as_view()),
    # payment
    path('<str:domain>/payment/type/', payment_type_list.PaymentTypeClientListAPIView.as_view()),
]
