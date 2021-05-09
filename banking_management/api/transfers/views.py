from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import NewTransferForm, TransferHistoryForm
from .models import Transfer
from ..accounts.models import Account


def list_transfer_request(request):
    transfer_list = Transfer.objects.all()
    context = {'transfer_list': transfer_list}
    return render(request, "transfer/transfer_list.html", context)


def create_transfer_request(request):
    if request.method == "POST":
        form = NewTransferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Creation successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful creation. Invalid information.")
    form = NewTransferForm
    transfer_list = Transfer.objects.all()
    context = {'transfer_list': transfer_list, 'transfer_form': form}
    return render(request, "transfer/transfer_creation.html", context)


def get_transfer_history_request(request):
    transfer_list = None
    select_account = None
    if request.method == "POST":
        form = TransferHistoryForm(request.POST)
        if form.is_valid():
            transfer_list, select_account = form.get_history()
            messages.success(request, "Ok !")
        else:
            messages.error(request, "Invalid information. Select an account number")

    form = TransferHistoryForm
    account_list = Account.objects.all()
    context = {'transfer_list': transfer_list,
               'account_list': account_list,
               'transfer_form': form,
               'selected_account': select_account}
    return render(request, "transfer/transfer_history.html", context)
