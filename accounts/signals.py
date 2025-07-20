from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ManagerProfile

@receiver(post_save, sender=User)
def create_manager_profile(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        ManagerProfile.objects.create(user=instance)
