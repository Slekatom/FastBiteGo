from django.urls import path
from .views import *

app_name = "payment"

urlpatterns = [
    path("", PaymentCreate.as_view(), name ="payment")
]