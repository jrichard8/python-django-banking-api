import datetime

from django import forms
from django.db.models import Q
from django.forms.utils import ErrorList

from .models import Transfer
from ..accounts.models import Account


class NewTransferForm(forms.ModelForm):
    """Form to create a New transfer."""
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
        amount = self.data.get('amount')
        new_balance = float(self.ta.balance) + float(amount)
        formatted_date = datetime.date.today().strftime("%Y-%m-%d")
        Transfer(amount=amount, from_account=self.fa, to_account=self.ta, date=formatted_date).save()
        self.ta.balance = new_balance
        self.ta.save()
        self.fa.balance = float(self.fa.balance) - float(amount)
        self.fa.save()

    def is_valid(self):
        amount = self.data.get('amount')
        if amount is None:
            return False
        from_account_id = self.data.get('from_account')
        to_account_id = self.data.get('to_account')
        if from_account_id is None or to_account_id is None:
            return False
        if from_account_id == to_account_id:
            return False
        if float(amount) <= 0:
            return False
        fa = Account.objects.get(account_no=from_account_id)
        ta = Account.objects.get(account_no=to_account_id)
        self.fa = fa
        self.ta = ta
        if float(fa.balance) < float(amount):
            return False
        return True


class TransferHistoryForm(forms.ModelForm):
    """Form to create to fetch transfer history for a given account_no."""
    class Meta:
        model = Account
        fields = ('account_no',)

    def get_history(self):
        account_id = self.data.get('account_no')
        transfer_list = list(Transfer.objects
                             .filter(Q(from_account=account_id) | Q(to_account=account_id))
                             .order_by('date'))
        return transfer_list, account_id

    def is_valid(self):
        if self.data.get('account_no') is None:
            return False
        return True
