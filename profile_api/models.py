from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=256, null=True)
    country = models.CharField(max_length=256, null=True)

    def __self__(self):
        return self.user.username
