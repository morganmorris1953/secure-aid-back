from django.contrib.auth.models import Group


confirmed_veteran_group, created = Group.objects.get_or_create(name="Veteran")


def is_confirmed_veteran(user):
    return user.groups.filter(name="Veteran").exists()
