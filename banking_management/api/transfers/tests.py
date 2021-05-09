import datetime
import decimal
import uuid
from uuid import uuid4

from django.test import Client
from django.test import TestCase

from .models import Transfer
from ..accounts.models import Account
from ..customers.models import Customer

acc_no1 = uuid4()
acc_no2 = uuid4()
today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")


class TransferTestCase(TestCase):

    def setUp(self):
        self.customer_me = Customer.objects.create(name="me",
                                                   age="42")
        self.customer_other = Customer.objects.create(name="other",
                                                      age="42")
        self.account_acc1 = Account.objects.create(account_no=acc_no1,
                                                   customer=self.customer_me,
                                                   balance="5500",
                                                   creation_date=today_str)
        self.account_acc2 = Account.objects.create(account_no=acc_no2,
                                                   customer=self.customer_other,
                                                   balance="1020",
                                                   creation_date=today_str)
        Transfer.objects.create(amount="1200",
                                from_account=self.account_acc1,
                                to_account=self.account_acc2,
                                date=today_str)
        Transfer.objects.create(amount="2000",
                                from_account=self.account_acc2,
                                to_account=self.account_acc1,
                                date=today_str)
        self.client = Client()

    def test_transfer_object_creation(self):
        """Test transfer creation in DB."""
        transfers = Transfer.objects.all()
        self.assertEqual(len(transfers), 2)
        self.assertEqual(transfers[0].amount, 1200)
        self.assertEqual(transfers[1].amount, 2000)

    def test_list_transfer(self):
        """Test return of endpoint /transfers/."""
        response = self.client.get('/transfers/')
        transfer_list = list(response.context['transfer_list'])
        self.assertEqual(len(transfer_list), 2)
        self.assertEqual(transfer_list[0].amount, 1200)
        self.assertEqual(uuid.UUID(str(transfer_list[0].to_account)), acc_no2)
        self.assertEqual(uuid.UUID(str(transfer_list[0].from_account)), acc_no1)
        self.assertEqual(transfer_list[1].amount, 2000)
        self.assertEqual(uuid.UUID(str(transfer_list[1].to_account)), acc_no1)
        self.assertEqual(uuid.UUID(str(transfer_list[1].from_account)), acc_no2)

    def test_create_transfer(self):
        """Test return and behavior of endpoint /transfer/new."""
        self.client.post('/transfers/new',
                         {"amount": 1000,
                          "from_account": acc_no1,
                          "to_account": acc_no2})
        response = self.client.get('/transfers/')
        transfer_list = list(response.context['transfer_list'])
        self.assertEqual(len(transfer_list), 3)
        self.assertEqual(transfer_list[2].amount, 1000)
        self.assertEqual(uuid.UUID(str(transfer_list[2].to_account)), acc_no2)
        self.assertEqual(uuid.UUID(str(transfer_list[2].from_account)), acc_no1)
        balance_response_acc2 = self.client.post('/accounts/balance', {"account_no": acc_no2})
        new_balance_acc2 = balance_response_acc2.context['balance']
        self.assertEqual(new_balance_acc2, 2020.00)
        balance_response_acc1 = self.client.post('/accounts/balance', {"account_no": acc_no1})
        new_balance_acc1 = balance_response_acc1.context['balance']
        self.assertEqual(new_balance_acc1, 4500.00)

    def test_create_transfer_fail_amount_too_large(self):
        response_post = self.client.post('/transfers/new',
                         {"amount": 10000,
                          "from_account": acc_no1,
                          "to_account": acc_no2})
        messages = list(response_post.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Unsuccessful creation. Invalid information.')
        response = self.client.get('/transfers/')
        transfer_list = list(response.context['transfer_list'])
        self.assertEqual(len(transfer_list), 2)

    def test_create_transfer_fail_same_acc_id(self):
        response_post = self.client.post('/transfers/new',
                         {"amount": 1000,
                          "from_account": acc_no1,
                          "to_account": acc_no1})
        messages = list(response_post.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Unsuccessful creation. Invalid information.')
        response = self.client.get('/transfers/')
        transfer_list = list(response.context['transfer_list'])
        self.assertEqual(len(transfer_list), 2)

    def test_get_transfer_history(self):
        """Test return and behavior of endpoint /transfer/history."""
        response = self.client.post('/transfers/history',
                                    {"account_no": acc_no1})
        transfer_list = list(response.context['transfer_list'])
        account = response.context['selected_account']
        self.assertEqual(len(transfer_list), 2)
        self.assertEqual(uuid.UUID(str(account)), acc_no1)



