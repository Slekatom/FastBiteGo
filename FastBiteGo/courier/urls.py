from django.urls import path
from .views import *

app_name = "courier"

urlpatterns = [
    path("requests/", RequestList.as_view(), name = "requests")
]