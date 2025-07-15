from django.db import models
from inventory.models import Product
from django.contrib.auth.models import User


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.user.username