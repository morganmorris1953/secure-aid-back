import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from ticket_api.models import Ticket

def validate_message_content(content):
    if content is None or content == "" or content.isspace():
        raise ValidationError(
            'Content is empty/invalid',
            code='invalid',
            params={'content': content},
        )


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True,
        null=False,
        default=uuid.uuid4,
        editable=False
    )
    room = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='chat_room',
    )
    
    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name='message_history',
        on_delete=models.CASCADE
    )
    content = models.TextField(validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    @classmethod
    def last_50_messages(cls, room_id):
        return cls.objects.filter(room_id=room_id).order_by('created_at').all()[:50]
    def __str__(self):
        return self.author

class UserMessages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # last_read_date = models.DateTimeField(
    #     auto_now_add=True,
    #     blank=False,
    #     null=False
    # )
    # def __str__(self):
    #     return self.User
