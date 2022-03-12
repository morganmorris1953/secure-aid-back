from rest_framework import permissions, viewsets
from .serializers import TicketSerializer
from .models import Ticket

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.all()
        aid_provider_id = self.request.query_params.get('aid_provider_id')
        aid_recipient_id = self.request.query_params.get('aid_recipient_id')
        sponsor_id = self.request.query_params.get('sponsor_id')
        if aid_provider_id is not None:
            queryset = queryset.filter(aid_provider_id=aid_provider_id)
        if aid_recipient_id is not None:
            queryset = queryset.filter(aid_recipient_id=aid_recipient_id)
        if sponsor_id is not None:
            queryset = queryset.filter(sponsor_id=sponsor_id)
        
        return queryset