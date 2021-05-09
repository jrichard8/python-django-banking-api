from django.urls import path

from .views import list_transfer_request, create_transfer_request, get_transfer_history_request

urlpatterns = [
    path('', list_transfer_request),
    path('new', create_transfer_request),
    path('history', get_transfer_history_request)
]