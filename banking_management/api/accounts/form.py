import datetime
from uuid import uuid4

from django import forms
from django.contrib.auth.models import User

from .models import Account

from ..customers.models import Customer


class NewAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('customer', 'balance')

    def save(self, commit=True):
        customer_id = self.data['customer']
        balance = self.data['balance']
        uuid = uuid4()
        customer = Customer.objects.get(id=customer_id)
        formatted_date = datetime.date.today().strftime("%Y-%m-%d")
        acc = Account(account_no=uuid, balance=balance, customer=customer, creation_date=formatted_date)
        acc.save()


class AccountBalanceForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('account_no',)

