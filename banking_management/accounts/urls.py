from django.urls import path

from . import views
from .views import AccountList, AccountDetail

urlpatterns = [
    path('', AccountList.as_view()),
    path('<uuid:pk>/', AccountDetail.as_view()),
]
