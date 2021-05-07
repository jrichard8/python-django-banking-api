from django import forms

from .models import Customer


class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'age')

    def save(self, commit=True):
        name = self.data['name']
        age = self.data['age']
        Customer(name=name, age=age).save()
