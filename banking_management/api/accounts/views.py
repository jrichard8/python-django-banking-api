from django.contrib import messages
from django.shortcuts import render, redirect

from .form import NewAccountForm
from .models import Account
from ..customers.models import Customer


def list_account_request(request):
    account_list = Account.objects.all()
    context = {'account_list': account_list}
    return render(request, "accounts/account_list.html", context)


def create_account_request(request):
    if request.method == "POST":
        form = NewAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Creation successful.")
            return redirect("home")
        # messages.error(request, "Unsuccessful creation. Invalid information.")
    form = NewAccountForm
    customer_list = Customer.objects.all()
    context = {'customer_list': customer_list, 'account_form': form}
    return render(request, "accounts/account_creation.html", context)
