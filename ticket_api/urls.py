from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet


router = DefaultRouter()
router.register(r'ticket', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]