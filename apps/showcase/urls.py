from django.urls import path, include
from apps.showcase.api.products_client_list import ProductsClientListAPIView
from apps.showcase.api.categories_client_list import CategoriesClientListAPIView
from apps.showcase.api.categories_client_detail import CategoriesClientDetailAPIView
from apps.showcase.api.banners_client_list import BannersClientListAPIView
from apps.showcase.api.banners_client_detail import BannersClientDetailAPIView
from apps.showcase.api.social_links_client_list import SocialLinksClientListAPIView
from apps.showcase.api.analytics_client_list import AnalyticsClientListAPIView
from apps.showcase.api.design_client_detail import DesignClientDetailAPIView
from apps.showcase.api.extra_phone_client_list import ExtraPhoneClientListAPIView
from apps.showcase.api.working_hours_client_list import WorkingHoursClientListAPIView
from apps.showcase.api.requisites_client_list import RequisitesClientListAPIView

app_name = 'showcase'

urlpatterns = [
    # main page
    path('products/', ProductsClientListAPIView.as_view()),
    path('categories/', CategoriesClientListAPIView.as_view()),
    path('categories/<str:slug>/', CategoriesClientDetailAPIView.as_view()),
    path('banners/', BannersClientListAPIView.as_view()),
    path('analytics/', AnalyticsClientListAPIView.as_view()),
    path('design/<int:pk>/', DesignClientDetailAPIView.as_view()),

    # main page pop ups
    # banner
    path('banners/<int:pk>/', BannersClientDetailAPIView.as_view()),
    # company info
    path('social-links/', SocialLinksClientListAPIView.as_view()),
    path('extra-phones/', ExtraPhoneClientListAPIView.as_view()),
    path('working-hours/', WorkingHoursClientListAPIView.as_view()),
    path('requisites/', RequisitesClientListAPIView.as_view()),

    # order (cart) detail/add/delete
    path('order/', include('apps.order.urls', namespace='order')),
]
