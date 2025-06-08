from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path('', views.MenuList.as_view(), name = "landing"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name = "category"),
    path("meal/<int:pk>/", views.MealDetailView.as_view(), name = "meal")
]