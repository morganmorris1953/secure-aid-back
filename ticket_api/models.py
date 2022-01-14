from django.db import models
from django.conf import settings
# from chat_api import Rooms

CATEGORIES = (
    ("Medical", "Medical"),
    ("Legal","Legal"),
    ("Finacial","Finacial")
)

STATUSES = (
    ("Awaiting","Awaiting"),
    ("In-Progess","In-Progess"),
    ("Complete","Complete")
)

class Ticket(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORIES)
    need_by_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUSES, default="Awaiting")
    sponsor_comments = models.TextField(null=True, blank=True)
    provider_comments = models.TextField(null=True, blank=True)
    aid_recipient_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Recipient_in_Ticket")
    aid_provider_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="Provider_in_Ticket")
    sponsor_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="Sponsor_in_Ticket")

    def __str__(self):
        return f"Ticket:{id} created:{self.created_on} recipient:{self.aid_recipient_id} status:{self.status} Provider:{self.aid_provider_id}"