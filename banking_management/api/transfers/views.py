from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import NewTransferForm
from .models import Transfer


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
