# api/serializers.py
from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_no', 'user', 'balance', 'creation_date')
