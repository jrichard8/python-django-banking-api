import datetime
from uuid import uuid4

from django import forms

from .models import Account
from ..customers.models import Customer


class NewAccountForm(forms.ModelForm):
    """
    Form for new account creation.
    It take customer_id and balance as input.
    """
    class Meta:
        model = Account
        fields = ('customer', 'balance')

    def save(self, commit=True):
        customer_id = self.data.get('customer')
        balance = self.data.get('balance')
        uuid = uuid4()
        customer = Customer.objects.get(id=customer_id)
        formatted_date = datetime.date.today().strftime("%Y-%m-%d")
        acc = Account(account_no=uuid, balance=balance, customer=customer, creation_date=formatted_date)
        acc.save()

    def is_valid(self):
        if self.data.get('customer') is None or self.data.get('balance') is None:
            return False
        return True


class AccountBalanceForm(forms.ModelForm):
    """
    Form for getting balance of a given account.
    It take account_no as input.
    """
    class Meta:
        model = Account
        fields = ('account_no',)

    def get_balance(self):
        account_id = self.data['account_no']
        account = Account.objects.get(account_no=account_id)
        return account.balance, account_id

    def is_valid(self):
        if self.data.get('account_no') is None:
            return False
        return True
