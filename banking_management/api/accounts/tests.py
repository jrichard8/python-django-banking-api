import datetime
import uuid
from uuid import uuid4

from django.test import Client
from django.test import TestCase

from .models import Account
from ..customers.models import Customer

acc_no1 = uuid4()
acc_no2 = uuid4()
today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")


class AccountTestCase(TestCase):
    def setUp(self):
        self.customer_me = Customer.objects.create(name="me",
                                           age="42")
        self.customer_other = Customer.objects.create(name="other",
                                           age="42")
        Account.objects.create(account_no=acc_no1,
                               customer=self.customer_me,
                               balance="2500",
                               creation_date=today_str)
        Account.objects.create(account_no=acc_no2,
                               customer=self.customer_other,
                               balance="1020",
                               creation_date=today_str)
        self.client = Client()

    def test_account_object_creation(self):
        """Animals that can speak are correctly identified"""
        acc = Account.objects.get(account_no=acc_no1)
        self.assertEqual(acc.balance, 2500)
        self.assertEqual(acc.creation_date, today)
        self.assertEqual(acc.customer.age, 42)

    def test_list_account(self):
        response = self.client.get('/accounts/')
        account_list = list(response.context['account_list'])
        self.assertEqual(len(account_list), 2)
        self.assertEqual(uuid.UUID(str(account_list[0])), acc_no1)

    def test_create_account(self):
        response = self.client.get('/accounts/new')
        customer_list = list(response.context['customer_list'])
        self.assertEqual(len(customer_list), 2)
        self.assertEqual(str(customer_list[0]), "me")
        self.client.post('/accounts/new', {"customer": self.customer_other.id, "balance": "10000"})
        response_acc = self.client.get('/accounts/')
        account_list = list(response_acc.context['account_list'])
        self.assertEqual(len(account_list), 3)
        self.assertNotEqual(uuid.UUID(str(account_list[2])), acc_no1)
        self.assertNotEqual(uuid.UUID(str(account_list[2])), acc_no2)

    def test_get_balance(self):
        response = self.client.get('/accounts/balance')
        account_list = list(response.context['account_list'])
        self.assertEqual(len(account_list), 2)
        balance_response = self.client.post('/accounts/balance', {"account_no": acc_no1})
        balance = balance_response.context['balance']
        selected_account = balance_response.context['selected_account']
        self.assertEqual(balance, 2500)
        self.assertEqual(uuid.UUID(str(selected_account)), acc_no1)
