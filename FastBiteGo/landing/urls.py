from django.urls import path
from . import views

app_name = "landing"

urlpatterns = [
    path('', views.AboutView.as_view(), name = "landing"),
]