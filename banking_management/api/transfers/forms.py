import datetime

from django import forms
from django.contrib import messages
from django.forms.utils import ErrorList
from rest_framework.exceptions import ValidationError

from .models import Transfer
from ..accounts.models import Account


class NewTransferForm(forms.ModelForm):



    class Meta:
        model = Transfer
        fields = ('amount', 'from_account', 'to_account')

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None, use_required_attribute=None,
                 renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        self.ta = None
        self.fa = None

    def save(self, commit=True):
        amount = self.data['amount']
        new_balance = float(self.ta.balance) + float(amount)
        self.ta.balance = new_balance
        self.ta.save()
        formatted_date = datetime.date.today().strftime("%Y-%m-%d")
        Transfer(amount=amount, from_account=self.fa, to_account=self.ta, date=formatted_date).save()

    def is_valid(self):
        amount = self.data['amount']
        from_account_id = self.data['from_account']
        to_account_id = self.data['to_account']
        fa = Account.objects.get(account_no=from_account_id)
        ta = Account.objects.get(account_no=to_account_id)
        self.fa = fa
        self.ta = ta
        if float(fa.balance) < float(amount):
            return False
        return True


