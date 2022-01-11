from rest_framework import permissions, viewsets
from .serializers import TicketSerializer
from .models import Ticket

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.all()