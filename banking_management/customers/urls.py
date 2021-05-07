# api/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CustomerList

urlpatterns = [
    path('', CustomerList.as_view())
]
