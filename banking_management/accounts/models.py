import uuid

from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    account_no = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for account')
    user = models.ForeignKey(
        User,  on_delete=models.SET_NULL, null=True
    )
    balance = models.DecimalField(
        default=0,
        max_digits=19,
        decimal_places=2
    )
    creation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.account_no)

