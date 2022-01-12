import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from 

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
        
    )
    
    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name='author_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField(validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def last_50_messages():
        return Message.objects.order_by('-created_at').all()[:50]

class UserMessages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # last_read_date = models.DateTimeField(
    #     auto_now_add=True,
    #     blank=False,
    #     null=False
    # )
    # def __str__(self):
    #     return self.User
