from django.db import models

from ..accounts.models import Account


class Transfer(models.Model):
    amount = models.DecimalField(
        default=0,
        max_digits=19,
        decimal_places=2
    )
    from_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='from_account'
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='to_account'
    )
    date = models.DateField(null=True, blank=True)
