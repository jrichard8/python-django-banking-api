from django.contrib import messages
from django.shortcuts import render, redirect

from .form import NewAccountForm, AccountBalanceForm
from .models import Account
from ..customers.models import Customer


def list_account_request(request):
    """
    return a list of all accounts
    """
    account_list = Account.objects.all()
    context = {'account_list': account_list}
    return render(request, "accounts/account_list.html", context)


def create_account_request(request):
    """
    Create a new Account.
    POST /account/new
    {
    "customer": <customer_id>,
    "balance": "10000"
    }
    """
    if request.method == "POST":
        form = NewAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Creation successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful creation. Invalid information.")
    form = NewAccountForm
    customer_list = Customer.objects.all()
    context = {'customer_list': customer_list, 'account_form': form}
    return render(request, "accounts/account_creation.html", context)


def get_balance_request(request):
    """
    Return balance of a given account.
    POST /account/balance
    {
        "account_no": <account_id>
    }
    """
    balance = None
    select_account = None
    if request.method == "POST":
        form = AccountBalanceForm(request.POST)
        if form.is_valid():
            balance, select_account = form.get_balance()
            messages.success(request, "Ok !")
        else:
            messages.error(request, "Invalid information. Select an account number")

    form = AccountBalanceForm
    account_list = Account.objects.all()
    context = {'account_list': account_list,
               'account_form': form,
               'balance': balance,
               'selected_account': select_account}
    return render(request, "accounts/account_balance.html", context)
