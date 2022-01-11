from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket

## Serializes current user Model
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','groups']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id',
            'created_on',
            'title',
            'category',
            'need_by_date',
            'status',
            'sponsor_comments',
            'provider_comments',
            'aid_recipient_id',
            'aid_provider_id'
        ]

