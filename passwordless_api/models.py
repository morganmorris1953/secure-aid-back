from django.contrib.auth.models import Group


# Create your models here.
approved_recipient, created = Group.objects.get_or_create(name="Recipient")


def is_approved_recipient(user):
    return user.groups.filter(name="Recipient").exists()
