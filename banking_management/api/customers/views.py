from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import NewCustomerForm
from .models import Customer


def list_customer_request(request):
    customer_list = Customer.objects.all()
    context = {'customer_list': customer_list}
    return render(request, "customer/customer_list.html", context)


def create_customer_request(request):
    if request.method == "POST":
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Creation successful.")
            return redirect("home")
        # messages.error(request, "Unsuccessful creation. Invalid information.")
    form = NewCustomerForm
    customer_list = Customer.objects.all()
    context = {'customer_list': customer_list, 'customer_form': form}
    return render(request, "customer/customer_creation.html", context)