from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet


router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='tickets')

