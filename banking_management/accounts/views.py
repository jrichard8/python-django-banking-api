from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
from .models import Account


def index(request):
    account_list = Account.objects.order_by('-creation_date')
    template = loader.get_template('accounts/index.html')
    context = {
        'account_list': account_list,
    }
    return HttpResponse(template.render(context, request))
