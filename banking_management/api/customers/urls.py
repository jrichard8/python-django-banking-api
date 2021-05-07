# api/urls.py
from django.urls import path

from .views import list_customer_request, create_customer_request

urlpatterns = [
    path('', list_customer_request),
    path('new', create_customer_request)
]
