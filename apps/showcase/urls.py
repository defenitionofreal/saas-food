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
                               products_client_detail)

app_name = 'showcase'

urlpatterns = [
    # main page
    path('products/', products_client_list.ProductsClientListAPIView.as_view()),
    path('categories/', categories_client_list.CategoriesClientListAPIView.as_view()),
    path('categories/<str:slug>/', categories_client_detail.CategoriesClientDetailAPIView.as_view()),
    path('banners/', banners_client_list.BannersClientListAPIView.as_view()),
    path('analytics/', analytics_client_list.AnalyticsClientListAPIView.as_view()),

    # change design to create or update view so no pk in url !
    path('design/<int:pk>/', design_client_detail.DesignClientDetailAPIView.as_view()),

    # main page pop ups
    # banner
    path('banners/<int:pk>/', banners_client_detail.BannersClientDetailAPIView.as_view()),
    # product
    path('products/<int:pk>/', products_client_detail.ProductClientDetailAPIView.as_view()),

    # company info
    path('social-links/', social_links_client_list.SocialLinksClientListAPIView.as_view()),
    path('extra-phones/', extra_phone_client_list.ExtraPhoneClientListAPIView.as_view()),
    path('working-hours/', working_hours_client_list.WorkingHoursClientListAPIView.as_view()),
    path('requisites/', requisites_client_list.RequisitesClientListAPIView.as_view()),

    # order (cart) detail/add/delete
    path('order/', include('apps.order.urls', namespace='order')),
]
