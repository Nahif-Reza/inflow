from django.db import models
from django.contrib.auth.models import User


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return f"Manager: {self.user.username}"

