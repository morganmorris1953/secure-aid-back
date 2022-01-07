from django.urls import path

from .views import HomeView, DashboardView

urlpatterns = [
    path("", HomeView.as_view(), name="home-view"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
]
