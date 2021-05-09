from django import forms

from .models import Customer


class NewCustomerForm(forms.ModelForm):
    """Form to create a New customer."""
    class Meta:
        model = Customer
        fields = ('name', 'age')

    def save(self, commit=True):
        name = self.data.get('name')
        age = self.data.get('age')
        Customer(name=name, age=age).save()

    def is_valid(self):
        if self.data.get('name') is None or self.data.get('age') is None:
            return False
        return True
