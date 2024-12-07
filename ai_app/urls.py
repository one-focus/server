# ai_app/urls.py

from django.urls import path
from .views import ai_endpoint

urlpatterns = [
    path('ai', ai_endpoint, name='ai_endpoint'),
]
