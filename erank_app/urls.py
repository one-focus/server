# erank_app/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ShopListingViewSet

router = DefaultRouter()
router.register(r'shop-listings', ShopListingViewSet, basename='shop-listing')

urlpatterns = [
    path('', include(router.urls)),
]
