from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import User


class Referral(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sponsored")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipients")


approved_recipient, created = Group.objects.get_or_create(name="Recipient")


def is_approved_recipient(user):
    return user.groups.filter(name="Recipient").exists()
