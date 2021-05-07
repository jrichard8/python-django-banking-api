from django.urls import path

from .views import list_account_request, create_account_request

urlpatterns = [
    path('', list_account_request),
    path('new', create_account_request)
]
