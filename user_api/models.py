from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.
class Referral(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sponsored")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipients")


veteran_group, created = Group.objects.get_or_create(name="Veteran")
recipient_group, created = Group.objects.get_or_create(name="Recipient")
provider_group, created = Group.objects.get_or_create(name="Provider")


def is_veteran(user):
    return user.groups.filter(name="Veteran").exists()


def is_recipient(user):
    return user.groups.filter(name="Recipient").exists()


def is_provider(user):
    return user.groups.filter(name="Provider").exists()
