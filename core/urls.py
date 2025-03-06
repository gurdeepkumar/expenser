from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("visual_expenses", views.home, name="visual_expenses"),
]
