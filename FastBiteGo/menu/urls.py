from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path('', views.MenuList.as_view(), name = "landing"),
    path("<int:pk>/", views.CategoryDetailView.as_view(), name = "meals"),
]