from django.test import Client
from django.test import TestCase

from .models import Customer


class CustomersTestCase(TestCase):

    def setUp(self):
        Customer.objects.create(name="me",
                                age="42")
        Customer.objects.create(name="other",
                                age="23")
        self.client = Client()

    def test_customer_object_creation(self):
        """Test customers creation in DB."""
        customers = Customer.objects.all()
        self.assertEqual(len(customers), 2)

    def test_list_customer(self):
        """Test return of endpoint /customers."""
        response = self.client.get('/customers/')
        customer_list = list(response.context['customer_list'])
        self.assertEqual(len(customer_list), 2)
        self.assertEqual(str(customer_list[0]), "me")
        self.assertEqual(str(customer_list[1]), "other")

    def test_create_customers(self):
        """Test return and behavior of endpoint /customer/new."""
        self.client.post('/customers/new', {"name": "jane", "age": "24"})
        response = self.client.get('/customers/')
        customer_list = list(response.context['customer_list'])
        self.assertEqual(len(customer_list), 3)
        self.assertEqual(str(customer_list[2]), "jane")
