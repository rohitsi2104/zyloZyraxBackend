from django.urls import path
from .views import (
    get_banners,
    get_offers,
)


urlpatterns = [
    path('banners/', get_banners, name='get_banners'),
    path('offers/', get_offers, name='get_offers'),
]