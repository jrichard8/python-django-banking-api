from django.db import models


class Customer(models.Model):
    """structure defining a client."""
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self):
        return self.name
